from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

from analyzer import analyze_dataframe, analyze_timeline


COLUMN_RENAME = {
    "TA (Sys)": "TA_Sys",
    "TA (Dia)": "TA_Dia",
    "Médicament": "Medicament",
    "Dose (ml)": "Dose_ml",
    "Concentration (mg/mL)": "Concentration_mg_ml",
    "Volume de perfusion": "Volume_perfusion",
    "Température": "Temp",
}


def load_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    return df.rename(columns=COLUMN_RENAME)


def main():
    try:
        csv_name = sys.argv[1] if len(sys.argv) > 1 else "TEST.csv"
        csv_path = Path(csv_name)

        if not csv_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {csv_path}")

        df = load_csv(csv_path)

        results = analyze_dataframe(df)

        print("\n===== RÉSULTATS =====\n")
        print(f"Fichier analysé : {csv_path.name}\n")

        for patient_id, result in sorted(results.items(), key=lambda x: x[0]):
            print(f"Patient {patient_id}")
            print(f"Heure : {result['Heure']}")
            print(f"Médicament : {result['Medicament']}")
            print(f"Administration : {result['Administration']}")
            print(f"Score : {result['score']}")
            print(f"Statut : {result['status']}")

            if result["alerts"]:
                print("Alertes :")
                for alert in result["alerts"]:
                    print(f" - {alert}")
            else:
                print("Alertes : aucune")

            print("-" * 40)

        timeline = analyze_timeline(df)

        output_dir = Path("rules/output")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / "timeline_results.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(timeline, f, ensure_ascii=False, indent=4)

        summary_file = output_dir / "results.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print(f"\nFichiers créés avec succès :")
        print(f" - {output_file.resolve()}")
        print(f" - {summary_file.resolve()}")

    except Exception as e:
        print("\nERREUR dans main.py :")
        print(e)


if __name__ == "__main__":
    main()
