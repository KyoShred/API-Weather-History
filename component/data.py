import json


def load_data():
    """
    Charge les données du fichier JSON et les retourne sous forme de dictionnaire.

    Returns:
      dict: Le dictionnaire contenant les données.
    """

    with open("data/rdu-weather-history.json", "r") as file:
        data = json.load(file)

    return data


def write_data(data):
    """
    Écrit les données dans le fichier JSON.

    Args:
      data (dict): Le dictionnaire contenant les données.
    """

    with open("data/rdu-weather-history.json", "w") as file:
        json.dump(data, file, indent=4)
    return data