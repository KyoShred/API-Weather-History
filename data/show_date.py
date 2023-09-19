from fastapi import FastAPI, Query
from typing import List
import json

app = FastAPI()

# Charger les données JSON depuis le fichier
with open("rdv-weather-history.json", "r") as json_file:
    donnees_json = json.load(json_file)

@app.get("/show/")
async def show(date_debut: str = Query(None, description="Date de début au format 'YYYY-MM-DD'"),
                            date_fin: str = Query(None, description="Date de fin au format 'YYYY-MM-DD'")):
    donnees_filtrees = []

    if date_debut and date_fin:
        # Filtrer les données en fonction des dates de début et de fin
        for item in donnees_json:
            if date_debut <= item["date"] <= date_fin:
                donnees_filtrees.append(item)
    else:
        # Si aucune date de début ou de fin n'est spécifiée, renvoyer toutes les données
        donnees_filtrees = donnees_json

    return donnees_filtrees
