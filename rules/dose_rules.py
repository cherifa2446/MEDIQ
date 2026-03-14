from __future__ import annotations

DOSE_RULES = {
    # Les doses sont exprimées en mg calculés à partir de dose_ml * concentration_mg_ml.
    # Quand l'énoncé clinique dépend du poids, du pH, du glucose ou d'un autre paramètre absent du CSV,
    # on ne peut pas faire une validation stricte. On garde alors seulement les bornes fixes défendables.
    "Adénosine": {
        "Bolus": {"min": 6, "max": 18, "label": "6 mg puis 12-18 mg IV"},
    },
    "Amiodarone": {
        "Bolus": {"min": 150, "max": 150, "label": "150 mg IV"},
    },
    "Ativan": {
        "Bolus": {"min": 1, "max": 4, "label": "1-4 mg IV"},
        "IM": {"min": 1, "max": 4, "label": "1-4 mg IM"},
    },
    "Atropine": {
        "Bolus": {"min": 0.5, "max": 3, "label": "0.5-3 mg"},
    },
    "Bicarbonnate de sodium": {
        # Le document donne 0.5-1 mEq/kg ≈ 42-84 mg/kg, donc dépend du poids.
        # Sans poids on évite une règle dure. On garde une plage très permissive pour détecter l'absurde total.
        "Bolus": {"min": 20, "max": 10000, "label": "dose dépend du poids"},
    },
    "Chlorure de calcium": {
        "Bolus": {"min": 1000, "max": 2000, "label": "1-2 g IV"},
    },
    "Dextrose": {
        # Dépend du poids, donc seulement garde-fou pour doses manifestement aberrantes.
        "Bolus": {"min": 5000, "max": 100000, "label": "dose dépend du poids"},
    },
    "Diltiazem": {
        # Le document donne 0.25 mg/kg IV; sans poids on met une plage adulte plausible.
        "Bolus": {"min": 10, "max": 30, "label": "≈0.25 mg/kg IV"},
    },
    "Épinéphrine": {
        "Bolus": {"min": 0.05, "max": 1.0, "label": "bolus critique"},
        "IM": {"min": 0.1, "max": 0.5, "label": "IM adulte plausible"},
    },
    "Fentanyl": {
        # Pas encore documenté par l'utilisateur.
    },
    "Insuline": {
        # Pas encore documenté par l'utilisateur.
    },
    "Naloxone": {
        "Bolus": {"min": 0.04, "max": 2.0, "label": "0.04-2 mg"},
        "IM": {"min": 0.04, "max": 2.0, "label": "0.04-2 mg"},
    },
    "Norépinéphrine": {
        # Perfusion seulement dans votre test; pas de détection d'erreur en perfusion selon l'énoncé.
    },
    "Phényléphrine": {
        "Bolus": {"min": 0.05, "max": 0.5, "label": "bolus IV plausible"},
    },
    "Propofol": {
        "Bolus": {"min": 20, "max": 200, "label": "20-200 mg"},
    },
    "Rocuronium": {
        "Bolus": {"min": 30, "max": 120, "label": "30-120 mg"},
    },
    "Soluté physiologique": {},
    "Sulfate de magnésium": {
        "Bolus": {"min": 1000, "max": 4000, "label": "1-4 g"},
    },
}


def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def check_dose(medicament, dose_ml, concentration_mg_ml, administration):
    """
    Vérifie si la dose est plausible pour le médicament et la voie d'administration.

    Retourne None si rien de suspect ou non applicable.
    Retourne un dict sinon.
    """

    if medicament is None or administration is None:
        return {
            "status": "warning",
            "score": 1,
            "message": "Donnée manquante pour vérifier la dose",
            "dose_mg": None,
        }

    administration = str(administration).strip()

    # Le défi dit qu'on n'a pas à détecter d'erreurs dans les perfusions.
    if administration.lower() == "perfusion":
        return None

    if medicament not in DOSE_RULES:
        return None

    med_rules = DOSE_RULES[medicament]
    if administration not in med_rules:
        return None

    dose_mg = _safe_float(dose_ml)
    concentration = _safe_float(concentration_mg_ml)
    if dose_mg is None or concentration is None:
        return {
            "status": "warning",
            "score": 1,
            "message": "Dose ou concentration invalide",
            "dose_mg": None,
        }

    dose_mg *= concentration
    rule = med_rules[administration]
    dose_min = rule["min"]
    dose_max = rule["max"]
    label = rule.get("label", f"{dose_min}-{dose_max} mg")

    # Pour les règles dépendant du poids, la fenêtre est volontairement large.
    if dose_mg < dose_min:
        return {
            "status": "warning",
            "score": 2,
            "message": (
                f"Dose possiblement trop faible pour {medicament} ({administration}) : "
                f"{dose_mg:.2f} mg (référence: {label})"
            ),
            "dose_mg": dose_mg,
        }

    if dose_mg > dose_max:
        severity = 4 if dose_mg >= dose_max * 2 else 3
        return {
            "status": "error",
            "score": severity,
            "message": (
                f"Dose trop élevée pour {medicament} ({administration}) : "
                f"{dose_mg:.2f} mg (référence: {label})"
            ),
            "dose_mg": dose_mg,
        }

    return None
