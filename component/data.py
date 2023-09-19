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

