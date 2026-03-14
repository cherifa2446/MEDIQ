import pandas as pd
import json
from pathlib import Path
from analyzer import analyze_dataframe, analyze_timeline


def main():
    try:
        df = pd.read_csv("TEST.csv")

        df = df.rename(columns={
            "TA (Sys)": "TA_Sys",
            "TA (Dia)": "TA_Dia",
            "Médicament": "Medicament",
            "Dose (ml)": "Dose_ml",
            "Concentration (mg/mL)": "Concentration_mg_ml",
            "Volume de perfusion": "Volume_perfusion",
            "Température": "Temp"
        })

        # Résumé final par patient
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

        # Timeline complète
        timeline = analyze_timeline(df)

        output_dir = Path("rules/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "timeline_results.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(timeline, f, ensure_ascii=False, indent=4)

        print(f"\nFichier créé avec succès : {output_file.resolve()}")

    except Exception as e:
        print("\nERREUR dans main.py :")
        print(e)


if __name__ == "__main__":
    main()