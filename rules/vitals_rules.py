from __future__ import annotations


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def infer_context(fc, tas, fr, sat):
    contexts = set()

    if fc is not None and fc < 60:
        contexts.add("bradycardie")
    if fc is not None and fc > 100:
        contexts.add("tachycardie")
    if tas is not None and tas < 90:
        contexts.add("hypotension")
    if fr is not None and fr < 12:
        contexts.add("depression_respiratoire")
    if sat is not None and sat < 92:
        contexts.add("hypoxemie")
    if (fr is not None and fr < 12) or (sat is not None and sat < 92):
        contexts.add("detresse_respiratoire")
    if (fr is not None and fr >= 12) and (sat is not None and sat >= 92):
        contexts.add("respiration_relativement_stable")

    return contexts


def _msg(status, score, message):
    return {"status": status, "score": score, "message": message}


def check_vitals(medicament, fc, tas, tad, fr, sat, temp, administration):
    """
    Validation clinique ligne par ligne uniquement à partir des signes vitaux courants.
    On n'utilise jamais les lignes futures, conformément au défi.
    """
    fc = _f(fc)
    tas = _f(tas)
    tad = _f(tad)
    fr = _f(fr)
    sat = _f(sat)
    temp = _f(temp)

    if None in (fc, tas, tad, fr, sat, temp):
        return _msg("warning", 1, "Signes vitaux invalides ou incomplets")

    contexts = infer_context(fc, tas, fr, sat)
    med = str(medicament).strip() if medicament is not None else ""
    admin = str(administration).strip().lower() if administration is not None else ""

    # Perfusions: pas d'erreur médicamenteuse demandée dans l'évaluation pour ce mode.
    if admin == "perfusion":
        return None

    if med == "Adénosine":
        if fc < 50:
            return _msg("error", 4, f"Adénosine contre-indiquée si FC < 50 bpm (FC = {fc})")
        if tas < 90:
            return _msg("error", 4, f"Adénosine contre-indiquée en hypotension (TAS = {tas} mmHg)")
        if fc <= 100:
            return _msg("warning", 2, f"Adénosine donnée sans tachycardie claire (FC = {fc} bpm)")

    if med == "Amiodarone":
        if fc < 50:
            return _msg("error", 4, f"Amiodarone contre-indiquée si FC < 50 bpm (FC = {fc})")
        if tas < 90:
            return _msg("error", 4, f"Amiodarone contre-indiquée en hypotension (TAS = {tas} mmHg)")

    if med == "Ativan":
        if fr < 14 and "detresse_respiratoire" in contexts:
            return _msg("error", 4, f"Ativan risqué si FR < 14 avec dépression respiratoire (FR = {fr}, SAT = {sat}%)")
        if tas < 90:
            return _msg("warning", 2, f"Ativan peu conseillé si patient hémodynamiquement instable (TAS = {tas} mmHg)")

    if med == "Atropine":
        if fc > 100:
            return _msg("error", 4, f"Atropine à éviter si FC > 100 bpm (FC = {fc})")
        if fc >= 60:
            return _msg("warning", 2, f"Atropine donnée sans bradycardie claire (FC = {fc} bpm)")

    if med == "Bicarbonnate de sodium":
        # La vraie contre-indication mentionnée dépend du pH > 7, absent du CSV.
        # On ne peut donc pas interdire proprement sur la base des seules colonnes disponibles.
        return None

    if med == "Chlorure de calcium":
        # Document fourni: pas de contre-indications signalées.
        return None

    if med == "Dextrose":
        # La règle dépend du glucose > 14, absent du CSV.
        return None

    if med == "Diltiazem":
        if tas < 90:
            return _msg("error", 4, f"Diltiazem contre-indiqué en hypotension sévère / choc (TAS = {tas} mmHg)")
        if fc < 40:
            return _msg("error", 4, f"Diltiazem contre-indiqué si FC < 40 bpm (FC = {fc})")
        if fc <= 100:
            return _msg("warning", 2, f"Diltiazem donné sans tachycardie nette (FC = {fc} bpm)")

    if med == "Épinéphrine":
        if tas > 180:
            return _msg("error", 4, f"Épinéphrine à ne pas donner en contexte hypertensif (TAS = {tas} mmHg)")

    if med == "Fentanyl":
        # Pas encore documenté dans ton doc incomplet.
        return None

    if med == "Insuline":
        # Dépend du glucose, absent du CSV.
        return None

    if med == "Naloxone":
        if fr >= 12 and sat >= 95:
            return _msg("warning", 2, f"Naloxone donnée sans signe respiratoire évident (FR = {fr}, SAT = {sat}%)")

    if med == "Norépinéphrine":
        return None

    if med == "Phényléphrine":
        if fc < 50:
            return _msg("warning", 2, f"Phényléphrine donnée avec FC très basse (FC = {fc} bpm)")

    if med == "Propofol":
        if tas < 90:
            return _msg("error", 4, f"Propofol contre-indiqué en hypotension (TAS = {tas} mmHg)")
        if fr < 12 or sat < 92:
            return _msg("warning", 2, f"Propofol dans un contexte respiratoire fragile (FR = {fr}, SAT = {sat}%)")

    if med == "Rocuronium":
        # Avec les données actuelles, on ne peut pas savoir s'il s'agit d'une induction/intubation voulue.
        # On signale seulement un contexte respiratoire déjà très fragile comme haut risque.
        if sat < 90 or fr < 10:
            return _msg("warning", 2, f"Rocuronium donné avec état respiratoire déjà critique (FR = {fr}, SAT = {sat}%)")

    if med == "Soluté physiologique":
        return None

    if med == "Sulfate de magnésium":
        if fc <= 100:
            return _msg("warning", 2, f"Sulfate de magnésium donné sans tachycardie claire / torsade suspecte (FC = {fc} bpm)")

    return None
