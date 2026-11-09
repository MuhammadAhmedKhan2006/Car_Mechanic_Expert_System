# -*- coding: utf-8 -*-
# api.py - diagnosis engine: sessions, question flow, scoring, final result
#
# The UI (app.py) only draws what api.py returns. All decision-making
# lives here and in knowledge_base/decision_rules.py.

from knowledge_base.questions import GENERAL_QUESTIONS, DIRECT_QUESTIONS, REPORT_QUESTIONS
from knowledge_base.symptoms import SYMPTOMS
from knowledge_base.vehicle_problems import PROBLEMS, CARDS, CARD_PROBLEMS
from knowledge_base.decision_rules import apply_answer, apply_symptom, apply_report_value, ranked_problems, priority_level
from knowledge_base.recommendations import RECOMMENDATIONS, SAFETY_NOTE, URGENT_WARNING

# Mode 2: which Mode-1 question card to reuse for follow-up questions
FOLLOW_CARD = {
    "battery": "electrical", "starter": "start", "fuel": "start",
    "engine_perf": "engine", "overheating": "overheat", "braking": "brake",
    "noise_vibration": "noise", "electrical": "electrical", "tyres": "tyre",
    "steering": "steering", "transmission": "gear", "ac": "ac",
    "exhaust": "exhaust", "oil_leak": "oil",
}

MAX_CONFIRM_SYMPTOMS = 8      # Mode 2: how many symptom checks to show
MIN_TOP_SCORE = 3             # below this the result is "not enough information"


# ------------------------------------------------------------------
# session helpers
# ------------------------------------------------------------------
def new_session(mode, lang="en", card=None):
    # mode: 'guided' (I don't know) or 'direct' (I have an idea)
    s = {
        "mode": mode, "lang": lang, "card": card,
        "stage": "pick" if mode == "direct" else "general",
        "answers": {},          # question_id -> answer (yes/no/not_sure/float)
        "order": [],            # question ids in the order they were answered
        "history": [],          # (stage_before, qid) for the Back button
        "scores": {},
        "candidates": [],       # Mode 2 possible problems after general questions
        "sym_pool": [],         # Mode 2 symptom ids to confirm
        "sym_index": 0,
        "follow_card": None,
        "result": None,
    }
    return s


def _find_question(qid):
    # Look a question id up in every bank (returns dict or None)
    for q in GENERAL_QUESTIONS:
        if q["id"] == qid: return q
    for card_qs in DIRECT_QUESTIONS.values():
        for q in card_qs:
            if q["id"] == qid: return q
    for card_q in REPORT_QUESTIONS.values():
        if card_q["id"] == qid: return card_q
    for sym in SYMPTOMS:
        if sym["id"] == qid: return sym
    return None


def recompute_scores(sess):
    # Rebuild scores from scratch by replaying every stored answer.
    # Simple and always consistent (used after Back / on load).
    scores = {}
    for qid, val in sess["answers"].items():
        if qid.startswith("sym_"):
            apply_symptom(qid, val, scores)
        elif qid.startswith("rp_"):
            apply_report_value(qid, float(val), scores)
        else:
            apply_answer(qid, val, scores)
    sess["scores"] = scores
    return scores


def _direct_question_list(card):
    # The ordered question list for a Mode-1 card: 5 yes/no + 1 report input
    qs = list(DIRECT_QUESTIONS.get(card, []))
    if card in REPORT_QUESTIONS:
        qs.append(REPORT_QUESTIONS[card])
    return qs


def current_question(sess):
    # Return the question the UI should show now, or None when finished.
    stage = sess["stage"]
    if stage == "pick" or stage == "rank" or stage == "result":
        return None
    if sess["mode"] == "direct":
        if stage == "questions":
            for q in _direct_question_list(sess["card"]):
                if q["id"] not in sess["answers"]:
                    return q
            sess["stage"] = "result"
            return None
    else:  # guided mode
        if stage == "general":
            for q in GENERAL_QUESTIONS:
                if q["id"] not in sess["answers"]:
                    return q
            # all general questions done -> move to candidate ranking
            _finish_general(sess)
            return None
        if stage == "confirm":
            while sess["sym_index"] < len(sess["sym_pool"]):
                sid = sess["sym_pool"][sess["sym_index"]]
                if sid not in sess["answers"]:
                    for sym in SYMPTOMS:
                        if sym["id"] == sid:
                            return sym
                sess["sym_index"] += 1
            _finish_confirm(sess)
            return None
        if stage == "follow":
            card = sess["follow_card"]
            for q in _direct_question_list(card):
                if q["id"] not in sess["answers"]:
                    return q
            sess["stage"] = "result"
            return None
    return None


def next_question(sess):
    # Keep advancing internal stages until a real question appears
    # (or the session reaches pick / result).
    for _ in range(20):
        q = current_question(sess)
        if q is not None:
            return q
        if sess["stage"] in ("pick", "result"):
            return None
        # stage just changed (rank -> confirm -> follow ...); loop again
    return None


def _finish_general(sess):
    # Mode 2 step 2: turn general answers into possible problems
    recompute_scores(sess)
    ranked = ranked_problems(sess["scores"])
    sess["candidates"] = [p for p, s in ranked[:4] if s > 0]
    if not sess["candidates"]:
        sess["stage"] = "result"      # not enough information
        return
    # symptom pool: symptoms linked to any candidate problem
    cand = set(sess["candidates"])
    pool = [s["id"] for s in SYMPTOMS if any(p in cand for p, _ in s["fx"])]
    sess["sym_pool"] = pool[:MAX_CONFIRM_SYMPTOMS]
    sess["sym_index"] = 0
    sess["stage"] = "confirm"


def _finish_confirm(sess):
    # Mode 2 step 4: ask follow-up questions of the current top problem
    recompute_scores(sess)
    ranked = ranked_problems(sess["scores"])
    if not ranked or ranked[0][1] < MIN_TOP_SCORE:
        sess["stage"] = "result"      # unclear answers -> no unsupported diagnosis
        return
    top_problem = ranked[0][0]
    sess["follow_card"] = FOLLOW_CARD.get(top_problem, "engine")
    sess["stage"] = "follow"


def submit_answer(sess, qid, value):
    # Store one answer, score it, save to DB, advance the flow.
    sess["history"].append((sess["stage"], qid))
    sess["answers"][qid] = value
    sess["order"].append(qid)

    # score it immediately (full recompute happens on stage changes)
    if qid.startswith("sym_"):
        apply_symptom(qid, value, sess["scores"])
    elif qid.startswith("rp_"):
        try:
            apply_report_value(qid, float(value), sess["scores"])
        except (TypeError, ValueError):
            pass
    else:
        apply_answer(qid, value, sess["scores"])

    # advance guided-mode internal indexes
    if sess["mode"] == "guided":
        if sess["stage"] == "confirm":
            sess["sym_index"] += 1
        # stage transitions are driven by current_question()


def go_back(sess):
    # Undo the last answer (used by the Back button), then fix the stage.
    if not sess["order"]:
        return
    qid = sess["order"].pop()
    sess["answers"].pop(qid, None)
    sess["history"].pop()
    if sess["mode"] == "guided" and sess["stage"] == "confirm":
        sess["sym_index"] = max(0, sess["sym_index"] - 1)
    recompute_scores(sess)
    stage_fix(sess)


def stage_fix(sess):
    # After going back, make sure the stage matches what is left to answer.
    if sess["mode"] == "direct":
        sess["stage"] = "questions" if sess.get("card") else "pick"
        return
    answered = set(sess["answers"])
    gen_done = all(q["id"] in answered for q in GENERAL_QUESTIONS)
    if not gen_done or "sym_pool" not in sess:
        sess["stage"] = "general"
        return
    remaining_syms = [sid for sid in sess["sym_pool"] if sid not in answered]
    if remaining_syms:
        sess["stage"] = "confirm"
        return
    card = sess.get("follow_card")
    if card:
        remaining_f = [q["id"] for q in _direct_question_list(card) if q["id"] not in answered]
        if remaining_f:
            sess["stage"] = "follow"
            return
    sess["stage"] = "result"


def pick_card(sess, card):
    # Mode 1: user selected a problem card -> start its questions
    sess["card"] = card
    sess["stage"] = "questions"


def build_result(sess):
    # Final diagnosis: most likely problem, evidence, alternatives,
    # recommendations, priority level and disclaimer.
    recompute_scores(sess)
    ranked = ranked_problems(sess["scores"])
    if not ranked or ranked[0][1] < MIN_TOP_SCORE:
        # Not enough information - do NOT invent a diagnosis
        res = {
            "enough": False,
            "en": "We could not find enough consistent signs to suggest a problem. Please describe the issue to a mechanic or answer again with more detail.",
            "ur": "ہمیں اتنی مستقل علامات نہیں ملیں کہ کوئی مسئلہ تجویز کیا جا سکے۔ براہ کرم میکینک کو مسئلہ بتائیں یا مزید تفصیل کے ساتھ دوبارہ جواب دیں۔",
        }
        sess["result"] = res
        return res

    top_problem, top_score = ranked[0]
    prob = PROBLEMS[top_problem]
    priority = priority_level(top_score, prob["critical"])

    # evidence: every 'yes' answer shown in words (question or symptom text)
    evidence = []
    for qid in sess["order"]:
        val = sess["answers"].get(qid)
        if val in ("yes", "not_sure"):
            q = _find_question(qid)
            if q:
                evidence.append({"qid": qid, "value": val,
                                 "en": q.get("en", qid), "ur": q.get("ur", qid)})
        elif qid.startswith("rp_"):
            q = _find_question(qid)
            if q:
                evidence.append({"qid": qid, "value": str(val) + " " + q.get("unit", ""),
                                 "en": q.get("en", qid), "ur": q.get("ur", qid)})

    # alternatives: next best problems (max 2), only if they scored
    alternatives = []
    for p, s in ranked[1:3]:
        alternatives.append({"id": p, "score": s,
                             "en": PROBLEMS[p]["en"], "ur": PROBLEMS[p]["ur"],
                             "simple_en": PROBLEMS[p]["simple_en"],
                             "simple_ur": PROBLEMS[p]["simple_ur"]})

    # chart data: top 5 problem scores for the result-page bar chart
    chart = [{"id": p, "score": sc} for p, sc in ranked[:5]]

    # recommendations for the top problem
    recs = []
    for r in RECOMMENDATIONS.get(top_problem, []):
        recs.append({"en": r["en"], "ur": r["ur"],
                     "why_en": r["why_en"], "why_ur": r["why_ur"], "prio": r["prio"]})
    if not recs:
        recs.append({"en": "Have the car inspected by a qualified mechanic.",
                     "ur": "گاڑی کی جانچ کسی مستند مکینک سے کروائیں۔",
                     "why_en": "A professional inspection confirms the cause.",
                     "why_ur": "پیشہ ور جانچ وجہ کی تصدیق کرتی ہے۔", "prio": "medium"})

    res = {
        "enough": True,
        "mode": sess["mode"],
        "problem": top_problem,
        "problem_en": prob["en"], "problem_ur": prob["ur"],
        "simple_en": prob["simple_en"], "simple_ur": prob["simple_ur"],
        "critical": prob["critical"],
        "score": top_score,
        "priority": priority,
        "evidence": evidence,
        "alternatives": alternatives,
        "chart": chart,
        "recommendations": recs,
        "disclaimer": SAFETY_NOTE,
        "urgent_warning": URGENT_WARNING if priority == "urgent" else None,
    }
    sess["result"] = res
    sess["stage"] = "result"
    return res


def total_questions():
    # How many questions exist in the whole bank (for the academic count)
    n = len(GENERAL_QUESTIONS)
    n += sum(len(v) for v in DIRECT_QUESTIONS.values())
    n += len(REPORT_QUESTIONS)
    n += len(SYMPTOMS)
    return n


def count_branches():
    # Rough count of conditional branches in decision_rules.py
    import inspect
    import knowledge_base.decision_rules as dr
    src = inspect.getsource(dr)
    return src.count("if ") + src.count("elif ")
