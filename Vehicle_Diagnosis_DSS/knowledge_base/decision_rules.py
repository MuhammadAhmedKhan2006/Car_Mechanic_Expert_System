# -*- coding: utf-8 -*-
# decision_rules.py - conditional decision-making rules (if / elif / else)
#
# apply_answer()      : scores a Yes/No/Not-Sure answer for a question id
# apply_symptom()     : scores a symptom confirmation in Mode 2
# apply_report_value(): scores a numeric report input
# priority_level()    : turns the top score into Low / Medium / High / Urgent
#
# "scores" is a dict {problem_id: points}. Higher points = more likely problem.

from .symptoms import SYMPTOMS


def bump(scores, problem, points):
    # Add points to a problem (never negative)
    scores[problem] = scores.get(problem, 0) + points


def apply_answer(qid, answer, scores):
    # --------------------------------------------------------------
    # MODE 2 - general questions (answer: yes / no / not_sure)
    # --------------------------------------------------------------
    if qid == 'g1':      # starts normally?
        if answer == 'no':
            bump(scores, 'battery', 3); bump(scores, 'starter', 3); bump(scores, 'fuel', 2)
        elif answer == 'not_sure':
            bump(scores, 'battery', 1); bump(scores, 'starter', 1)
    elif qid == 'g2':    # rough / shake / stall
        if answer == 'yes':
            bump(scores, 'engine_perf', 3); bump(scores, 'transmission', 1)
        elif answer == 'not_sure':
            bump(scores, 'engine_perf', 1)
    elif qid == 'g3':    # warning lights
        if answer == 'yes':
            bump(scores, 'electrical', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure':
            bump(scores, 'electrical', 1)
    elif qid == 'g4':    # overheating / steam
        if answer == 'yes':
            bump(scores, 'overheating', 4)
        elif answer == 'not_sure':
            bump(scores, 'overheating', 1)
    elif qid == 'g5':    # brakes feel wrong
        if answer == 'yes':
            bump(scores, 'braking', 4)
        elif answer == 'not_sure':
            bump(scores, 'braking', 1)
    elif qid == 'g6':    # unusual noises
        if answer == 'yes':
            bump(scores, 'noise_vibration', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure':
            bump(scores, 'noise_vibration', 1)
    elif qid == 'g7':    # exhaust smoke
        if answer == 'yes':
            bump(scores, 'exhaust', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure':
            bump(scores, 'exhaust', 1)
    elif qid == 'g8':    # AC warm / weak
        if answer == 'yes':
            bump(scores, 'ac', 4)
        elif answer == 'not_sure':
            bump(scores, 'ac', 1)
    elif qid == 'g9':    # gears / clutch
        if answer == 'yes':
            bump(scores, 'transmission', 4)
        elif answer == 'not_sure':
            bump(scores, 'transmission', 1)
    elif qid == 'g10':   # steering heavy / shake
        if answer == 'yes':
            bump(scores, 'steering', 3); bump(scores, 'tyres', 1)
        elif answer == 'not_sure':
            bump(scores, 'steering', 1)
    elif qid == 'g11':   # tyres worn / pull
        if answer == 'yes':
            bump(scores, 'tyres', 4); bump(scores, 'steering', 1)
        elif answer == 'not_sure':
            bump(scores, 'tyres', 1)
    elif qid == 'g12':   # slower / more fuel
        if answer == 'yes':
            bump(scores, 'engine_perf', 3); bump(scores, 'fuel', 1)
        elif answer == 'not_sure':
            bump(scores, 'engine_perf', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "start" (engine won't start)
    # --------------------------------------------------------------
    elif qid == 'st_q1':
        if answer == 'yes': bump(scores, 'battery', 4)
        elif answer == 'not_sure': bump(scores, 'battery', 1)
    elif qid == 'st_q2':
        if answer == 'yes': bump(scores, 'battery', 3); bump(scores, 'starter', 2)
        elif answer == 'not_sure': bump(scores, 'battery', 1)
    elif qid == 'st_q3':
        if answer == 'yes': bump(scores, 'fuel', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'fuel', 1)
    elif qid == 'st_q4':
        if answer == 'yes': bump(scores, 'fuel', 3)
        elif answer == 'not_sure': bump(scores, 'fuel', 1)
    elif qid == 'st_q5':
        if answer == 'yes': bump(scores, 'fuel', 2); bump(scores, 'engine_perf', 2)
        elif answer == 'not_sure': bump(scores, 'fuel', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "overheat"
    # --------------------------------------------------------------
    elif qid == 'ov_q1':
        if answer == 'yes': bump(scores, 'overheating', 4)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)
    elif qid == 'ov_q2':
        if answer == 'yes': bump(scores, 'overheating', 4)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)
    elif qid == 'ov_q3':
        if answer == 'yes': bump(scores, 'overheating', 3)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)
    elif qid == 'ov_q4':
        if answer == 'yes': bump(scores, 'overheating', 3); bump(scores, 'electrical', 1)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)
    elif qid == 'ov_q5':
        if answer == 'yes': bump(scores, 'overheating', 3)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "brake"
    # --------------------------------------------------------------
    elif qid == 'br_q1':
        if answer == 'yes': bump(scores, 'braking', 5)
        elif answer == 'not_sure': bump(scores, 'braking', 1)
    elif qid == 'br_q2':
        if answer == 'yes': bump(scores, 'braking', 3); bump(scores, 'noise_vibration', 1)
        elif answer == 'not_sure': bump(scores, 'braking', 1)
    elif qid == 'br_q3':
        if answer == 'yes': bump(scores, 'braking', 3); bump(scores, 'tyres', 1)
        elif answer == 'not_sure': bump(scores, 'braking', 1)
    elif qid == 'br_q4':
        if answer == 'yes': bump(scores, 'braking', 3); bump(scores, 'electrical', 1)
        elif answer == 'not_sure': bump(scores, 'braking', 1)
    elif qid == 'br_q5':
        if answer == 'yes': bump(scores, 'braking', 3)
        elif answer == 'not_sure': bump(scores, 'braking', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "noise"
    # --------------------------------------------------------------
    elif qid == 'nv_q1':
        if answer == 'yes': bump(scores, 'engine_perf', 3); bump(scores, 'noise_vibration', 2)
        elif answer == 'not_sure': bump(scores, 'engine_perf', 1)
    elif qid == 'nv_q2':
        if answer == 'yes': bump(scores, 'noise_vibration', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'noise_vibration', 1)
    elif qid == 'nv_q3':
        if answer == 'yes': bump(scores, 'tyres', 3); bump(scores, 'noise_vibration', 1)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)
    elif qid == 'nv_q4':
        if answer == 'yes': bump(scores, 'noise_vibration', 4)
        elif answer == 'not_sure': bump(scores, 'noise_vibration', 1)
    elif qid == 'nv_q5':
        if answer == 'yes': bump(scores, 'tyres', 2); bump(scores, 'noise_vibration', 2); bump(scores, 'steering', 1)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "electrical"
    # --------------------------------------------------------------
    elif qid == 'el_q1':
        if answer == 'yes': bump(scores, 'battery', 3)
        elif answer == 'not_sure': bump(scores, 'battery', 1)
    elif qid == 'el_q2':
        if answer == 'yes': bump(scores, 'electrical', 3); bump(scores, 'battery', 1)
        elif answer == 'not_sure': bump(scores, 'electrical', 1)
    elif qid == 'el_q3':
        if answer == 'yes': bump(scores, 'electrical', 3); bump(scores, 'battery', 1)
        elif answer == 'not_sure': bump(scores, 'electrical', 1)
    elif qid == 'el_q4':
        if answer == 'yes': bump(scores, 'electrical', 3)
        elif answer == 'not_sure': bump(scores, 'electrical', 1)
    elif qid == 'el_q5':
        if answer == 'yes': bump(scores, 'electrical', 4)
        elif answer == 'not_sure': bump(scores, 'electrical', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "tyre"
    # --------------------------------------------------------------
    elif qid == 'ty_q1':
        if answer == 'yes': bump(scores, 'tyres', 3)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)
    elif qid == 'ty_q2':
        if answer == 'yes': bump(scores, 'tyres', 5)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)
    elif qid == 'ty_q3':
        if answer == 'yes': bump(scores, 'tyres', 2); bump(scores, 'steering', 2)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)
    elif qid == 'ty_q4':
        if answer == 'yes': bump(scores, 'tyres', 3)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)
    elif qid == 'ty_q5':
        if answer == 'yes': bump(scores, 'tyres', 2); bump(scores, 'noise_vibration', 1)
        elif answer == 'not_sure': bump(scores, 'tyres', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "oil"
    # --------------------------------------------------------------
    elif qid == 'ol_q1':
        if answer == 'yes': bump(scores, 'oil_leak', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)
    elif qid == 'ol_q2':
        if answer == 'yes': bump(scores, 'exhaust', 3); bump(scores, 'oil_leak', 1); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'exhaust', 1)
    elif qid == 'ol_q3':
        if answer == 'yes': bump(scores, 'fuel', 3); bump(scores, 'engine_perf', 1); bump(scores, 'exhaust', 1)
        elif answer == 'not_sure': bump(scores, 'fuel', 1)
    elif qid == 'ol_q4':
        if answer == 'yes': bump(scores, 'oil_leak', 4)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)
    elif qid == 'ol_q5':
        if answer == 'yes': bump(scores, 'oil_leak', 3)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "ac"
    # --------------------------------------------------------------
    elif qid == 'ac_q1':
        if answer == 'yes': bump(scores, 'ac', 4)
        elif answer == 'not_sure': bump(scores, 'ac', 1)
    elif qid == 'ac_q2':
        if answer == 'yes': bump(scores, 'ac', 3)
        elif answer == 'not_sure': bump(scores, 'ac', 1)
    elif qid == 'ac_q3':
        if answer == 'yes': bump(scores, 'ac', 2)
        elif answer == 'not_sure': bump(scores, 'ac', 1)
    elif qid == 'ac_q4':
        if answer == 'yes': bump(scores, 'ac', 2)
        elif answer == 'not_sure': bump(scores, 'ac', 1)
    elif qid == 'ac_q5':
        if answer == 'yes': bump(scores, 'ac', 2)
        elif answer == 'not_sure': bump(scores, 'ac', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "steering"
    # --------------------------------------------------------------
    elif qid == 'sr_q1':
        if answer == 'yes': bump(scores, 'steering', 5)
        elif answer == 'not_sure': bump(scores, 'steering', 1)
    elif qid == 'sr_q2':
        if answer == 'yes': bump(scores, 'steering', 3)
        elif answer == 'not_sure': bump(scores, 'steering', 1)
    elif qid == 'sr_q3':
        if answer == 'yes': bump(scores, 'steering', 3); bump(scores, 'tyres', 1)
        elif answer == 'not_sure': bump(scores, 'steering', 1)
    elif qid == 'sr_q4':
        if answer == 'yes': bump(scores, 'steering', 4)
        elif answer == 'not_sure': bump(scores, 'steering', 1)
    elif qid == 'sr_q5':
        if answer == 'yes': bump(scores, 'steering', 3)
        elif answer == 'not_sure': bump(scores, 'steering', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "gear"
    # --------------------------------------------------------------
    elif qid == 'gc_q1':
        if answer == 'yes': bump(scores, 'transmission', 4)
        elif answer == 'not_sure': bump(scores, 'transmission', 1)
    elif qid == 'gc_q2':
        if answer == 'yes': bump(scores, 'transmission', 4)
        elif answer == 'not_sure': bump(scores, 'transmission', 1)
    elif qid == 'gc_q3':
        if answer == 'yes': bump(scores, 'transmission', 3)
        elif answer == 'not_sure': bump(scores, 'transmission', 1)
    elif qid == 'gc_q4':
        if answer == 'yes': bump(scores, 'transmission', 2); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'transmission', 1)
    elif qid == 'gc_q5':
        if answer == 'yes': bump(scores, 'transmission', 3); bump(scores, 'engine_perf', 1)
        elif answer == 'not_sure': bump(scores, 'transmission', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "engine" (performance / fuel use)
    # --------------------------------------------------------------
    elif qid == 'en_q1':
        if answer == 'yes': bump(scores, 'engine_perf', 3); bump(scores, 'transmission', 1)
        elif answer == 'not_sure': bump(scores, 'engine_perf', 1)
    elif qid == 'en_q2':
        if answer == 'yes': bump(scores, 'overheating', 3); bump(scores, 'ac', 1)
        elif answer == 'not_sure': bump(scores, 'overheating', 1)
    elif qid == 'en_q3':
        if answer == 'yes': bump(scores, 'oil_leak', 1); bump(scores, 'engine_perf', 2)
        elif answer == 'not_sure': bump(scores, 'engine_perf', 1)
    elif qid == 'en_q4':
        if answer == 'yes': bump(scores, 'engine_perf', 3); bump(scores, 'transmission', 1)
        elif answer == 'not_sure': bump(scores, 'engine_perf', 1)
    elif qid == 'en_q5':
        if answer == 'yes': bump(scores, 'engine_perf', 4)
        elif answer == 'not_sure': bump(scores, 'engine_perf', 1)

    # --------------------------------------------------------------
    # MODE 1 - card: "exhaust"
    # --------------------------------------------------------------
    elif qid == 'ex_q1':
        if answer == 'yes': bump(scores, 'oil_leak', 3); bump(scores, 'engine_perf', 2); bump(scores, 'exhaust', 1)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)
    elif qid == 'ex_q2':
        if answer == 'yes': bump(scores, 'fuel', 3); bump(scores, 'engine_perf', 2); bump(scores, 'exhaust', 1)
        elif answer == 'not_sure': bump(scores, 'fuel', 1)
    elif qid == 'ex_q3':
        if answer == 'yes': bump(scores, 'oil_leak', 4)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)
    elif qid == 'ex_q4':
        if answer == 'yes': bump(scores, 'oil_leak', 2); bump(scores, 'fuel', 2)
        elif answer == 'not_sure': bump(scores, 'oil_leak', 1)
    elif qid == 'ex_q5':
        if answer == 'yes': bump(scores, 'exhaust', 4)
        elif answer == 'not_sure': bump(scores, 'exhaust', 1)

    # Unknown question id -> no scoring (safe fallback)
    return scores


def apply_symptom(sym_id, answer, scores):
    # Score a symptom confirmation in Mode 2.
    # answer: 'yes' uses full points, 'not_sure' uses half (rounded down to 1 min).
    if answer == 'no':
        return scores
    factor = 1 if answer == 'yes' else 0   # not_sure gives no points, just stays neutral
    for sym in SYMPTOMS:
        if sym['id'] == sym_id:
            if answer == 'yes':
                for prob, pts in sym['fx']:
                    bump(scores, prob, pts)
            elif answer == 'not_sure':
                for prob, pts in sym['fx']:
                    bump(scores, prob, max(1, pts // 2))
            return scores
    return scores


def apply_report_value(qid, value, scores):
    # Score a numeric report input (value is a float).
    # --------------------------------------------------------------
    if qid == 'rp_start' or qid == 'rp_el':      # battery voltage
        if value < 11.0:
            bump(scores, 'battery', 4)
        elif value < 12.2:
            bump(scores, 'battery', 2)
        elif value > 15.0:
            bump(scores, 'electrical', 3)
    elif qid == 'rp_ov':                          # engine temperature
        if value >= 120:
            bump(scores, 'overheating', 5)
        elif value > 105:
            bump(scores, 'overheating', 3)
        elif value < 70:
            bump(scores, 'overheating', 1)
    elif qid == 'rp_br':                          # km since brake service
        if value >= 60000:
            bump(scores, 'braking', 3)
        elif value >= 30000:
            bump(scores, 'braking', 1)
    elif qid == 'rp_nv' or qid == 'rp_ol' or qid == 'rp_en':  # oil level / km
        if qid in ('rp_nv', 'rp_ol'):
            if value < 15:
                bump(scores, 'oil_leak', 4); bump(scores, 'engine_perf', 2)
            elif value < 30:
                bump(scores, 'oil_leak', 2); bump(scores, 'engine_perf', 1)
            elif value < 50:
                bump(scores, 'oil_leak', 1)
        else:
            if value >= 20000:
                bump(scores, 'engine_perf', 2); bump(scores, 'oil_leak', 1)
            elif value >= 10000:
                bump(scores, 'engine_perf', 1)
    elif qid == 'rp_ty' or qid == 'rp_sr':        # tyre pressure
        if value < 20:
            bump(scores, 'tyres', 4); bump(scores, 'steering', 1)
        elif value < 28:
            bump(scores, 'tyres', 2)
        elif value > 40:
            bump(scores, 'tyres', 2)
    elif qid == 'rp_ac' or qid == 'rp_gc' or qid == 'rp_ex':  # km since service
        if value >= 80000:
            bump(scores, 'ac' if qid == 'rp_ac' else ('transmission' if qid == 'rp_gc' else 'exhaust'), 2)
        elif value >= 40000:
            bump(scores, 'ac' if qid == 'rp_ac' else ('transmission' if qid == 'rp_gc' else 'exhaust'), 1)
    return scores


def priority_level(top_score, problem_critical):
    # Turn the winning score into a priority label.
    # Returns one of: low / medium / high / urgent
    if problem_critical and top_score >= 12:
        return 'urgent'
    if top_score >= 12:
        return 'high'
    if top_score >= 6:
        return 'medium'
    return 'low'


def ranked_problems(scores):
    # Return problems sorted by score (highest first), ignoring zero scores.
    items = [(p, s) for p, s in scores.items() if s > 0]
    items.sort(key=lambda x: x[1], reverse=True)
    return items
