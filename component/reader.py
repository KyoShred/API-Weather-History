
"""
  Cette fonction permet de consulter les données météorologiques en options avec filtrage par date.

  Args:
    data (dict): Dictionnaire JSON contenant les données météorologiques.
    dated (str, optional): Date de début de filtrage.
    datef (str, optional): Date de fin de filtrage.
    prcp (float, optional): La valeur de précipitation minimale.


  Returns:
    dict: Un dictionnaire JSON contenant les données météorologiques filtrées ( ou tout les données si aucun filtre n'est spécifié).

"""


def get_data(data):
    return {"message": f"Il y a {len(data)} releves", "date": data}


def get_date_data(data, dated: str = None, datef: str = None):
    """Retrieve all date within the given range

    Args:
        data (JSON): from JSON file.
        dated (str, required): Starting date. Defaults to None.
        datef (str, required): Ending date. Defaults to None.

    Returns:
        dict: message and date.
    """

    filtered_data = data

    if dated:
        filtered_data = [
            item for item in filtered_data if item.get("date") >= dated]

        if datef:
            filtered_data = [
                item for item in filtered_data if item.get('date') <= datef]

            return {"message": f"Il y'a {len(filtered_data)} releves entre le {dated} et le {datef}", "date": filtered_data}


def get_precipitation(data, prcp: float = None) -> dict:
    """
    Récupère les données de précipitations supérieures à une valeur donnée.

    """
    filtered_data = data
    if prcp:
        filtered_data = [item for item in data if item.get('prcp') == prcp]

    return {"message": f"Il y'a {len(filtered_data)} releves avec une precipitation egale a {prcp}", "date": filtered_data}


def get_temperature_range(data, mintemp: float = None, maxtemp: float = None) -> dict:
    """
    Récupère les données de température dans une plage donnée.

    Args:
      data (dict): Le dictionnaire JSON contenant les données de température.
      mintemp (float, optional): La valeur de température minimale.
      maxtemp (float, optional): La valeur de température maximale.

    Returns:
      dict: Un dictionnaire JSON contenant les données de température filtrées.

    """

    filtered_data = data

    if mintemp:
        filtered_data = [item for item in data if item.get('tmin') >= mintemp]

    if maxtemp:
        filtered_data = [item for item in data if item.get('tmax') <= maxtemp]

    return {"message": f"Il y'a {len(filtered_data)} releves avec une temperature minimale egale a {mintemp} et une temperature maximale egale a {maxtemp}", "date": filtered_data}
