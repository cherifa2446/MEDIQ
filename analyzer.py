from rules.dose_rules import check_dose
from rules.vitals_rules import check_vitals

def analyze_dataframe(df):
    results = {}

    for _, row in df.iterrows():
        score = 0
        alerts = []

        med = row["Medicament"]
        admin = row["Administration"]

        # Vérification dose
        dose_alert = check_dose(
            med,
            row["Dose_ml"],
            row["Concentration_mg_ml"],
            admin
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
            admin
        )

        if vitals_alert:
            score += vitals_alert["score"]
            alerts.append(vitals_alert["message"])

        # Statut final
        if score == 0:
            status = "Normal"
        elif score <= 2:
            status = "Inhabituel"
        else:
            status = "Erreur critique"

        patient_id = row["ID"]

        # garder seulement la ligne la plus suspecte par patient
        if patient_id not in results or score > results[patient_id]["score"]:
            results[patient_id] = {
                "Heure": row["Heure"],
                "Medicament": med,
                "score": score,
                "status": status,
                "alerts": alerts
            }

    return results