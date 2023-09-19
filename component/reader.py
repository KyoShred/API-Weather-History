
"""
  Cette fonction permet de consulter les données météorologiques en options avec filtrage par date.

  Args:
    data (dict): Dictionnaire JSON contenant les données météorologiques.
    dated (str, optional): Date de début de filtrage.
    datef (str, optional): Date de fin de filtrage.

  Returns:
    dict: Un dictionnaire JSON contenant les données météorologiques filtrées ( ou tout les données si aucun filtre n'est spécifié).

"""


def get_data(data):
    return {"message": f"Il y q {len(data)} releves", "date": data}


def get_date_data(data, dated: str = None, datef: str = None):

    filtered_data = data

    if dated:
        filtered_data = [
            item for item in filtered_data if item.get("date") >= dated]

    if datef:
        filtered_data = [
            item for item in filtered_data if item.get('date') <= datef]

        return {"message": f"Il y'a {len(filtered_data)} releves entre le {dated} et le {datef}", "date": filtered_data}


def get_precipitation(data, prcp: float):
    if prcp:
        filtered_data = [
            item for item in data if item.get('prcp') >= prcp]
        return {"message": f"Il y'a {len(filtered_data)} releves avec une precipitation superieur a {prcp}", "date": filtered_data}
