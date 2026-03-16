"""
Règles de dosage par médicament et voie d'administration.
Sources : document de posologie v2 (mis à jour).

Toutes les doses sont en mg (dose_mg = volume_ml × concentration_mg_mL).
Les perfusions sont exclues du contrôle (règle du défi).

Médicaments poids-dépendants : plage calculée pour adulte standard 50–100 kg.
"""

DOSE_RULES = {

    # ── ADÉNOSINE ──────────────────────────────
    # 6 mg IV → 12 mg → 12-18 mg
    "Adénosine": {
        "Bolus": {"min": 6, "max": 18},
    },

    # ── AMIODARONE ─────────────────────────────
    # Bolus : 150 mg IV (tolérance ±50%)
    "Amiodarone": {
        "Bolus": {"min": 100, "max": 300},
    },

    # ── ATIVAN ─────────────────────────────────
    # 1–4 mg IV / IM
    "Ativan": {
        "Bolus": {"min": 1, "max": 4},
        "IM":    {"min": 1, "max": 4},
    },

    # ── ATROPINE ───────────────────────────────
    # 0.5 mg → max 3 mg
    "Atropine": {
        "Bolus": {"min": 0.5, "max": 3},
    },

    # ── BICARBONATE DE SODIUM ──────────────────
    # 0.5–1 mEq/kg = 42–84 mg/kg
    # Adulte 50–100 kg → min 42×50=2100 mg, max 84×100=8400 mg
    "Bicarbonate de sodium": {
        "Bolus": {"min": 42, "max": 8400},
    },
    "Bicarbonnate de sodium": {  # alias CSV (double 'n')
        "Bolus": {"min": 42, "max": 8400},
    },

    # ── CHLORURE DE CALCIUM ────────────────────
    # 1–2 g IV = 1000–2000 mg
    "Chlorure de calcium": {
        "Bolus": {"min": 1000, "max": 2000},
    },

    # ── DEXTROSE ───────────────────────────────
    # 0.5–1 g/kg → adulte 50–100 kg → 25 000–100 000 mg
    "Dextrose": {
        "Bolus": {"min": 25000, "max": 100000},
    },

    # ── DILTIAZEM ──────────────────────────────
    # 0.25 mg/kg IV → adulte 50–100 kg → 12.5–25 mg
    "Diltiazem": {
        "Bolus": {"min": 12, "max": 30},
    },

    # ── ÉPINÉPHRINE ────────────────────────────
    # Bolus IV critique : 0.05–1.0 mg
    # IM : 0.1–0.5 mg (auto-injecteur)
    "Épinéphrine": {
        "Bolus": {"min": 0.05, "max": 1.0},
        "IM":    {"min": 0.1,  "max": 0.5},
    },

    # ── FENTANYL ───────────────────────────────
    # Bolus IV : 25–100 µg = 0.025–0.1 mg
    # Dose de maintien : 25–50 µg = 0.025–0.05 mg
    # Plage globale : 0.025–0.1 mg
    "Fentanyl": {
        "Bolus": {"min": 0.025, "max": 0.1},
        "IM":    {"min": 0.025, "max": 0.1},
    },

    # ── INSULINE ───────────────────────────────
    # 0.1 U/kg/h → max 10 U/kg/h
    # Concentration standard 100 U/mL → 1 U ≈ 0.0347 mg
    # En pratique urgence : bolus 5–10 U IV
    # Plage en mg : 0.17–3.47 mg (5–100 U)
    "Insuline": {
        "Bolus": {"min": 0.17, "max": 3.47},
    },

    # ── NALOXONE ───────────────────────────────
    # 0.04–2 mg IV ou IM, max 10 mg cumulatif
    "Naloxone": {
        "Bolus": {"min": 0.04, "max": 2.0},
        "IM":    {"min": 0.04, "max": 2.0},
    },

    # ── NORÉPINÉPHRINE ─────────────────────────
    # Perfusion uniquement → pas de règle bolus
    "Norépinéphrine": {},

    # ── PHÉNYLÉPHRINE ──────────────────────────
    # Bolus IV urgence : 0.05–0.5 mg (50–500 µg)
    "Phényléphrine": {
        "Bolus": {"min": 0.05, "max": 0.5},
    },

    # ── PROPOFOL ───────────────────────────────
    # Induction : 0.5–2.5 mg/kg → adulte 50–100 kg → 25–250 mg
    "Propofol": {
        "Bolus": {"min": 25, "max": 250},
    },

    # ── ROCURONIUM ─────────────────────────────
    # 0.45–1.2 mg/kg → adulte 50–100 kg → 22.5–120 mg
    "Rocuronium": {
        "Bolus": {"min": 22, "max": 120},
    },

    # ── SOLUTÉ PHYSIOLOGIQUE ───────────────────
    "Soluté physiologique": {},

    # ── SULFATE DE MAGNÉSIUM ───────────────────
    # 1–4 g IV = 1000–4000 mg
    "Sulfate de magnésium": {
        "Bolus": {"min": 1000, "max": 4000},
    },
}


def check_dose(medicament, dose_ml, concentration_mg_ml, administration):
    """
    Vérifie si la dose administrée est dans la plage plausible.
    dose_mg = dose_ml × concentration_mg_ml

    Retourne :
    - None si dose plausible ou non applicable
    - dict {status, score, message, dose_mg} sinon
    """

    if medicament is None or administration is None:
        return {
            "status": "warning",
            "score": 1,
            "message": "Données manquantes (médicament ou voie d'administration)",
            "dose_mg": None,
        }

    administration = str(administration).strip()

    if administration.lower() == "perfusion":
        return None

    if medicament not in DOSE_RULES:
        return None

    rules_for_med = DOSE_RULES[medicament]
    if not rules_for_med or administration not in rules_for_med:
        return None

    try:
        dose_mg = float(dose_ml) * float(concentration_mg_ml)
    except (TypeError, ValueError):
        return {
            "status": "warning",
            "score": 1,
            "message": f"Dose ou concentration illisible pour {medicament}",
            "dose_mg": None,
        }

    rule = rules_for_med[administration]
    dose_min = rule["min"]
    dose_max = rule["max"]

    if dose_mg < dose_min:
        return {
            "status": "warning",
            "score": 2,
            "message": (
                f"DOSE TROP FAIBLE — {medicament} ({administration}) : "
                f"{dose_mg:.3g} mg administrés "
                f"(plage attendue : {dose_min}–{dose_max} mg)"
            ),
            "dose_mg": dose_mg,
        }

    if dose_mg > dose_max:
        return {
            "status": "error",
            "score": 3,
            "message": (
                f"DOSE TROP ÉLEVÉE — {medicament} ({administration}) : "
                f"{dose_mg:.3g} mg administrés "
                f"(plage attendue : {dose_min}–{dose_max} mg)"
            ),
            "dose_mg": dose_mg,
        }

    return None