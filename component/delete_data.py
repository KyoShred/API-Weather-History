"""
exemple d'une API FastAPI permettent de supprimer des dates

"""
from datetime import date

from fastapi import FastAPI
import json

app = FastAPI()

#permet d'ouvrire le fichier JSON et le lire

with open("data/rdu-weather-history.json", "r") as file:
    data = json.load(file)

app.delete("data")
async def delete_data(dated : str= None, datef : str= None):
    """
    supprimer des données en fonction d'une intervalle de dates spécifiée.

    Args:
        dated:date de début de l'intervalle (ex : 2017-01-01)
        datef: date de fin de l'intervalle (ex : 2022-02-18)

    Returns:
        dict : message affichant combien de données ont été supprimées.
    """
    deleted_count = 0

    for item in data:
        if dated <= item['date'] <= datef:
            date.remove(item)
            deleted_count += 1

        return {'delected '}

    else:

        return {"delected : data"}