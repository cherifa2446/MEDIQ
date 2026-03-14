import pandas as pd

df = pd.read_csv("TEST.csv")

df = df.rename(columns={
    "TA (Sys)": "TA_Sys",
    "TA (Dia)": "TA_Dia",
    "Médicament": "Medicament",
    "Dose (ml)": "Dose_ml",
    "Concentration (mg/mL)": "Concentration_mg_ml",
    "Volume de perfusion": "Volume_perfusion"
})

print(df.columns.tolist())
print()
print(df.iloc[0])