from __future__ import annotations

from rules.dose_rules import check_dose
from rules.vitals_rules import check_vitals


STATUS_BY_SCORE = [
    (0, "Normal"),
    (2, "Inhabituel"),
    (99, "Erreur critique"),
]


def _status_from_score(score: int) -> str:
    if score == 0:
        return "Normal"
    if score <= 2:
        return "Inhabituel"
    return "Erreur critique"


def _analyze_row(row):
    score = 0
    alerts = []

    med = row["Medicament"]
    admin = row["Administration"]

    # Vérification dose
    dose_alert = check_dose(
        med,
        row["Dose_ml"],
        row["Concentration_mg_ml"],
        admin,
    )

    if dose_alert:
        score += dose_alert["score"]
        alerts.append(dose_alert["message"])

    # Vérification signes vitaux
    vitals_alert = check_vitals(
        med,
        row["FC"],
        row["TA_Sys"],
        row["TA_Dia"],
        row["FR"],
        row["SAT"],
        row["Temp"],
        admin,
    )

    if vitals_alert:
        score += vitals_alert["score"]
        alerts.append(vitals_alert["message"])

    status = _status_from_score(score)

    return {
        "ID": row["ID"],
        "Heure": row["Heure"],
        "Medicament": med,
        "Administration": admin,
        "FC": row["FC"],
        "TA_Sys": row["TA_Sys"],
        "TA_Dia": row["TA_Dia"],
        "FR": row["FR"],
        "SAT": row["SAT"],
        "Temp": row["Temp"],
        "score": score,
        "status": status,
        "alerts": alerts,
    }


def analyze_dataframe(df):
    """
    Analyse tout le dataframe et garde pour chaque patient
    la ligne avec le score d'erreur le plus élevé.
    """

    results = {}

    for _, row in df.iterrows():

        current = _analyze_row(row)
        patient_id = current["ID"]

        if patient_id not in results:
            results[patient_id] = current
            continue

        existing = results[patient_id]

        # garder la ligne la plus grave
        if current["score"] > existing["score"]:
            results[patient_id] = current

        elif current["score"] == existing["score"] and len(current["alerts"]) > len(existing["alerts"]):
            results[patient_id] = current

    return results


def analyze_timeline(df):
    """
    Analyse ligne par ligne pour générer une timeline
    complète de la prise en charge.
    """

    timeline = []

    for _, row in df.iterrows():
        timeline.append(_analyze_row(row))

    # tri par patient puis heure
    timeline.sort(key=lambda x: (x["ID"], x["Heure"]))

    return timeline
