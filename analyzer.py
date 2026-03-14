from rules.dose_rules import check_dose
from rules.vitals_rules import check_vitals


def analyze_dataframe(df):
    results = {}

    for _, row in df.iterrows():
        score = 0
        alerts = []

        med = row["Medicament"]
        admin = row["Administration"]

        dose_alert = check_dose(
            med,
            row["Dose_ml"],
            row["Concentration_mg_ml"],
            admin
        )

        if dose_alert:
            score += dose_alert["score"]
            alerts.append(dose_alert["message"])

        vitals_alert = check_vitals(
            med,
            row["FC"],
            row["TA_Sys"],
            row["TA_Dia"],
            row["FR"],
            row["SAT"],
            row["Temp"],
            admin
        )

        if vitals_alert:
            score += vitals_alert["score"]
            alerts.append(vitals_alert["message"])

        if score == 0:
            status = "Normal"
        elif score <= 2:
            status = "Inhabituel"
        else:
            status = "Erreur critique"

        patient_id = row["ID"]

        if patient_id not in results or score > results[patient_id]["score"]:
            results[patient_id] = {
                "Heure": row["Heure"],
                "Medicament": med,
                "score": score,
                "status": status,
                "alerts": alerts
            }

    return results


def analyze_timeline(df):
    timeline = []

    for _, row in df.iterrows():
        score = 0
        alerts = []

        med = row["Medicament"]
        admin = row["Administration"]

        dose_alert = check_dose(
            med,
            row["Dose_ml"],
            row["Concentration_mg_ml"],
            admin
        )

        if dose_alert:
            score += dose_alert["score"]
            alerts.append(dose_alert["message"])

        vitals_alert = check_vitals(
            med,
            row["FC"],
            row["TA_Sys"],
            row["TA_Dia"],
            row["FR"],
            row["SAT"],
            row["Temp"],
            admin
        )

        if vitals_alert:
            score += vitals_alert["score"]
            alerts.append(vitals_alert["message"])

        if score == 0:
            status = "Normal"
        elif score <= 2:
            status = "Inhabituel"
        else:
            status = "Erreur critique"

        timeline.append({
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
            "alerts": alerts
        })

    timeline.sort(key=lambda x: x["Heure"])

    return timeline