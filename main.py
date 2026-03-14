import pandas as pd
from analyzer import analyze_dataframe

def main():
    df = pd.read_csv("TEST.csv")

    df = df.rename(columns={
        "TA (Sys)": "TA_Sys",
        "TA (Dia)": "TA_Dia",
        "Médicament": "Medicament",
        "Dose (ml)": "Dose_ml",
        "Concentration (mg/mL)": "Concentration_mg_ml",
        "Volume de perfusion": "Volume_perfusion"
    })

    results = analyze_dataframe(df)

    print("\n===== RÉSULTATS =====\n")

    for patient_id, result in results.items():
        print(f"Patient {patient_id}")
        print(f"Heure : {result['Heure']}")
        print(f"Médicament : {result['Medicament']}")
        print(f"Score : {result['score']}")
        print(f"Statut : {result['status']}")

        if result["alerts"]:
            print("Alertes :")
            for alert in result["alerts"]:
                print(f" - {alert}")

        print("-" * 40)

if __name__ == "__main__":
    main()