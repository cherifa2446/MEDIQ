"""
Règles de contre-indications basées sur les signes vitaux.
Sources : document de posologie v2 (mis à jour).

Scores :
  1 = inhabituel / à surveiller
  2 = déconseillé / contre-indiqué relatif
  3 = contre-indiqué absolu / dangereux
"""


def check_vitals(medicament, fc, tas, tad, fr, sat, temp, administration):
    """
    Vérifie la cohérence entre le médicament et les signes vitaux du patient.

    Retourne :
    - None si aucun problème détecté
    - dict {status, score, message} sinon
    """

    try:
        fc  = float(fc)
        tas = float(tas)
        tad = float(tad)
        fr  = float(fr)
        sat = float(sat)
        temp = float(temp)
    except (TypeError, ValueError):
        return {
            "status": "warning",
            "score": 1,
            "message": "Signes vitaux invalides ou manquants — impossible de valider le médicament",
        }

    # Perfusions exclues (règle du défi)
    if str(administration).strip().lower() == "perfusion":
        return None

    # ── ADÉNOSINE ──────────────────────────────────────────────────
    # FC < 50 → NE PAS DONNER
    # TAS < 90 → NE PAS DONNER (baisse encore plus la pression)
    if medicament == "Adénosine":
        if fc < 50:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Adénosine avec FC = {fc:.0f} bpm "
                    f"(seuil : FC < 50). Risque d'asystolie."
                ),
            }
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Adénosine avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS < 90). Risque d'aggraver l'hypotension."
                ),
            }

    # ── AMIODARONE ─────────────────────────────────────────────────
    # FC < 50 → NE PAS DONNER
    # TAS < 90 → NE PAS DONNER
    if medicament == "Amiodarone":
        if fc < 50:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Amiodarone avec FC = {fc:.0f} bpm "
                    f"(seuil : FC < 50)."
                ),
            }
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Amiodarone avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS < 90). Risque d'aggraver l'hypotension."
                ),
            }

    # ── ATIVAN (lorazépam) ─────────────────────────────────────────
    # FR < 14 → NE PAS DONNER (déprime la respiration)
    # TAS < 90 (instabilité hémodynamique) → déconseillé
    if medicament == "Ativan":
        if fr < 14:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Ativan avec FR = {fr:.0f} resp/min "
                    f"(seuil : FR < 14). Risque de dépression respiratoire sévère."
                ),
            }
        if tas < 90:
            return {
                "status": "warning",
                "score": 2,
                "message": (
                    f"DÉCONSEILLÉ — Ativan avec TAS = {tas:.0f} mmHg "
                    f"(instabilité hémodynamique). Risque d'aggraver le choc."
                ),
            }

    # ── ATROPINE ───────────────────────────────────────────────────
    # Indiquée pour FC < 60 (bradycardie)
    # FC > 100 → NE PAS DONNER
    if medicament == "Atropine":
        if fc > 100:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Atropine avec FC = {fc:.0f} bpm "
                    f"(seuil : FC > 100). Risque d'aggraver la tachycardie."
                ),
            }
        if fc >= 60:
            return {
                "status": "warning",
                "score": 2,
                "message": (
                    f"INHABITUEL — Atropine sans bradycardie "
                    f"(FC = {fc:.0f} bpm ≥ 60). Indication clinique peu claire."
                ),
            }

    # ── BICARBONATE DE SODIUM ──────────────────────────────────────
    # CI en alcalose (pH > 7.45) — pas de pH dans le CSV
    # Proxy : FR élevée + SAT normale + hémodynamique stable = pas d'acidose évidente
    if medicament == "Bicarbonate de sodium":
        if fr >= 20 and sat >= 95 and tas >= 90:
            return {
                "status": "warning",
                "score": 1,
                "message": (
                    f"INHABITUEL — Bicarbonate sans signe évident d'acidose "
                    f"(FR = {fr:.0f}, SAT = {sat:.0f}%, TAS = {tas:.0f} mmHg). "
                    f"Vérifier le pH — CI si alcalose."
                ),
            }

    # ── DILTIAZEM ──────────────────────────────────────────────────
    # TAS < 90 → NE PAS DONNER (hypotension / choc cardiogénique)
    # FC < 40 → NE PAS DONNER
    if medicament == "Diltiazem":
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Diltiazem avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS < 90). Hypotension sévère / choc cardiogénique."
                ),
            }
        if fc < 40:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Diltiazem avec FC = {fc:.0f} bpm "
                    f"(seuil : FC < 40). Bradycardie sévère."
                ),
            }

    # ── ÉPINÉPHRINE ────────────────────────────────────────────────
    # TAS > 180 → NE PAS DONNER (hypertension)
    if medicament == "Épinéphrine":
        if tas > 180:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Épinéphrine avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS > 180). Risque d'aggravation hypertensive sévère."
                ),
            }

    # ── FENTANYL ───────────────────────────────────────────────────
    # FR < 10 → NE PAS DONNER (dépression respiratoire)
    # SAT < 85% → NE PAS DONNER
    if medicament == "Fentanyl":
        if fr < 10:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Fentanyl avec FR = {fr:.0f} resp/min "
                    f"(seuil : FR < 10). Dépression respiratoire déjà présente."
                ),
            }
        if sat < 85:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Fentanyl avec SAT = {sat:.0f}% "
                    f"(seuil : SAT < 85%). Hypoxémie sévère."
                ),
            }

    # ── INSULINE ───────────────────────────────────────────────────
    # CI si FC < 50 ou TAS < 90
    # (augmente contractilité cardiaque — besoin d'un substrat hémodynamique stable)
    if medicament == "Insuline":
        if fc < 50:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Insuline avec FC = {fc:.0f} bpm "
                    f"(seuil : FC < 50). Instabilité hémodynamique sévère."
                ),
            }
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Insuline avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS < 90). Maintenir TAS > 90 avant d'administrer."
                ),
            }

    # ── NALOXONE ───────────────────────────────────────────────────
    # Indiquée si FR < 12 (dépression respiratoire aux opioïdes)
    # Si FR ≥ 12 ET SAT ≥ 95% → indication peu claire
    if medicament == "Naloxone":
        if fr >= 12 and sat >= 95:
            return {
                "status": "warning",
                "score": 2,
                "message": (
                    f"INHABITUEL — Naloxone sans signe de dépression respiratoire "
                    f"(FR = {fr:.0f} resp/min ≥ 12, SAT = {sat:.0f}%). "
                    f"Indication peu claire."
                ),
            }

    # ── PHÉNYLÉPHRINE ──────────────────────────────────────────────
    # Vasoconstricteur pur → cause bradycardie réflexe
    # FC < 50 → déconseillé
    if medicament == "Phényléphrine":
        if fc < 50:
            return {
                "status": "warning",
                "score": 2,
                "message": (
                    f"DÉCONSEILLÉ — Phényléphrine avec FC = {fc:.0f} bpm "
                    f"(< 50). Risque de bradycardie réflexe aggravée."
                ),
            }

    # ── PROPOFOL ───────────────────────────────────────────────────
    # TAS < 90 → CONTRE-INDIQUÉ (effondrement hémodynamique)
    if medicament == "Propofol":
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Propofol avec TAS = {tas:.0f} mmHg "
                    f"(seuil : TAS < 90). Risque d'effondrement hémodynamique."
                ),
            }

    # ── ROCURONIUM ─────────────────────────────────────────────────
    # SAT < 90% → dangereux sans voies aériennes sécurisées
    if medicament == "Rocuronium":
        if sat < 90:
            return {
                "status": "error",
                "score": 3,
                "message": (
                    f"CONTRE-INDIQUÉ — Rocuronium avec SAT = {sat:.0f}% "
                    f"(seuil : SAT < 90%). Hypoxémie avant paralysie — intubation à haut risque."
                ),
            }

    # ── CHLORURE DE CALCIUM / SOLUTÉ PHYSIO / SULFATE MG ──────────
    # Pas de CI via signes vitaux selon le document

    return None