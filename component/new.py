import json
from component.data import write_data

data = write_data()


def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float, awnd: float):
    """
        Args:
        date(str): Date.
        tmin(float): Température minimale.
        tmax(float): Température maximale.
        prcp(float): Précipitation.
        snow(float): Neige.
        snwd(float): Accumulation de neige.
        awnd(float): Vitesse du vent moyen.

        Returns:
        dict: Message de confirmation.
        """

    new_entry = {
        "date": date,
        "tmin": tmin,
        "tmax": tmax,
        "prcp": prcp,
        "snow": snow,
        "snwd": snwd,
        "awnd": awnd
    }
    data.append(new_entry)
    with open("rdu-weather-history.json", "w") as file:
        json.dump(data, file, indent=4)
    return {"message": "Données ajoutées avec succès"}
