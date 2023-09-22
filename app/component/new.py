
def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float,
                      awnd: float):  # Ajout d'une donnée métérologique

    new_entry = {
        "date": date,
        "tmin": tmin,
        "tmax": tmax,
        "prcp": prcp,
        "snow": snow,
        "snwd": snwd,
        "awnd": awnd
    }