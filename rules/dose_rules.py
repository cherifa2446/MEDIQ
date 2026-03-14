DOSE_RULES = {
    # médicament: plages plausibles en mg selon voie d'administration
    "Adénosine": {
        "Bolus": {"min": 6, "max": 18}
    },
    "Amiodarone": {
        "Bolus": {"min": 150, "max": 300}
    },
    "Ativan": {
        "Bolus": {"min": 1, "max": 4},
        "IM":    {"min": 1, "max": 4}
    },
    "Atropine": {
        "Bolus": {"min": 0.5, "max": 3}
    },
    "Bicarbonate de sodium": {
        "Bolus": {"min": 40, "max": 100}
    },
    "Chlorure de calcium": {
        "Bolus": {"min": 500, "max": 2000}
    },
    "Dextrose": {
        "Bolus": {"min": 10000, "max": 50000}
    },
    "Diltiazem": {
        "Bolus": {"min": 15, "max": 25}
    },
    "Épinéphrine": {
        # bolus IV en contexte critique
        "Bolus": {"min": 0.05, "max": 1.0},
        # IM plus élevée possible
        "IM":    {"min": 0.1, "max": 0.5}
    },
    "Fentanyl": {
        "Bolus": {"min": 0.05, "max": 0.2}
    },
    "Insuline": {
        "Bolus": {"min": 1, "max": 20}
    },
    "Naloxone": {
        "Bolus": {"min": 0.04, "max": 2.0},
        "IM":    {"min": 0.04, "max": 2.0}
    },
    "Norépinéphrine": {
        
    },
    "Phényléphrine": {
        "Bolus": {"min": 0.1, "max": 0.5}
    },
    "Propofol": {
        "Bolus": {"min": 20, "max": 200}
    },
    "Rocuronium": {
        "Bolus": {"min": 30, "max": 120}
    },
    "Soluté physiologique": {
        
    },
    "Sulfate de magnésium": {
        "Bolus": {"min": 1000, "max": 4000}
    },
}


def check_dose(medicament, dose_ml, concentration_mg_ml, administration):
    """
    Vérifie si la dose est plausible pour le médicament et la voie d'administration.

    Retourne :
    - None si la dose semble plausible ou si non applicable
    - un dict {status, score, message, dose_mg} sinon
    """

    if medicament is None or administration is None:
        return {
            "status": "warning",
            "score": 1,
            "message": "Donnée manquante pour vérifier la dose",
            "dose_mg": None
        }

    administration = str(administration).strip()

    # Le défi dit qu'on n'a pas à détecter d'erreurs dans les perfusions
    if administration.lower() == "perfusion":
        return None

    if medicament not in DOSE_RULES:
        return None

    if administration not in DOSE_RULES[medicament]:
        return None

    try:
        dose_mg = float(dose_ml) * float(concentration_mg_ml)
    except (TypeError, ValueError):
        return {
            "status": "warning",
            "score": 1,
            "message": "Dose ou concentration invalide",
            "dose_mg": None
        }

    rule = DOSE_RULES[medicament][administration]
    dose_min = rule["min"]
    dose_max = rule["max"]

    if dose_mg < dose_min:
        return {
            "status": "warning",
            "score": 2,
            "message": (
                f"Dose trop faible pour {medicament} ({administration}) : "
                f"{dose_mg:.2f} mg (attendu {dose_min}–{dose_max} mg)"
            ),
            "dose_mg": dose_mg
        }

    if dose_mg > dose_max:
        return {
            "status": "error",
            "score": 3,
            "message": (
                f"Dose trop élevée pour {medicament} ({administration}) : "
                f"{dose_mg:.2f} mg (attendu {dose_min}–{dose_max} mg)"
            ),
            "dose_mg": dose_mg
        }

    return None