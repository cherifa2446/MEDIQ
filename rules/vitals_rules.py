def check_vitals(medicament, fc, tas, tad, fr, sat, temp, administration):
    """
    Vérifie si le médicament semble cohérent avec les signes vitaux.
    
    Retourne :
    - None si rien de suspect
    - un dict {status, score, message} sinon
    """

    try:
        fc = float(fc)
        tas = float(tas)
        tad = float(tad)
        fr = float(fr)
        sat = float(sat)
        temp = float(temp)
    except (TypeError, ValueError):
        return {
            "status": "warning",
            "score": 1,
            "message": "Signes vitaux invalides ou incomplets"
        }

    #  ATROPINE 
    if medicament == "Atropine":
        if fc >= 60:
            return {
                "status": "warning",
                "score": 2,
                "message": f"Atropine administrée mais FC = {fc} bpm (pas de bradycardie claire)"
            }

    # ÉPINÉPHRINE 
    if medicament == "Épinéphrine":
        if fc > 150:
            return {
                "status": "warning",
                "score": 2,
                "message": f"Épinéphrine administrée malgré FC très élevée ({fc} bpm)"
            }

    #  DILTIAZEM 
    if medicament == "Diltiazem":
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": f"Diltiazem administré malgré hypotension (TAS = {tas} mmHg)"
            }
        if fc < 60:
            return {
                "status": "error",
                "score": 3,
                "message": f"Diltiazem administré malgré bradycardie (FC = {fc} bpm)"
            }

    # AMIODARONE 
    if medicament == "Amiodarone":
        if tas < 85:
            return {
                "status": "warning",
                "score": 2,
                "message": f"Amiodarone administrée avec TAS basse ({tas} mmHg)"
            }

    # PROPOFOL 
    if medicament == "Propofol":
        if tas < 90:
            return {
                "status": "error",
                "score": 3,
                "message": f"Propofol administré malgré hypotension (TAS = {tas} mmHg)"
            }

    #  PHÉNYLÉPHRINE 
    if medicament == "Phényléphrine":
        if fc < 50:
            return {
                "status": "warning",
                "score": 2,
                "message": f"Phényléphrine administrée avec FC très basse ({fc} bpm)"
            }

    #  NALOXONE 
    if medicament == "Naloxone":
        if sat >= 95 and fr >= 12:
            return {
                "status": "warning",
                "score": 2,
                "message": f"Naloxone administrée sans signe respiratoire évident (SAT = {sat}%, FR = {fr})"
            }

    # ROCURONIUM 
    if medicament == "Rocuronium":
        if sat < 90 or fr < 10:
            return {
                "status": "error",
                "score": 3,
                "message": f"Rocuronium administré malgré hypoxémie/dépression respiratoire (SAT = {sat}%, FR = {fr})"
            }

    # BICARBONATE DE SODIUM 
    if medicament == "Bicarbonate de sodium":
        if fr < 12 and sat > 94:
            return {
                "status": "warning",
                "score": 1,
                "message": f"Bicarbonate administré dans un contexte peu évocateur (FR = {fr}, SAT = {sat}%)"
            }

    return None