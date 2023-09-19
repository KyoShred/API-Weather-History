"""
Exemple d'une API FastAPI utilisant un fichier JSON pour fournir des données et permettant le filtrage par date.

"""

from fastapi import FastAPI
import json

app = FastAPI()

#permet d'ouvrire le fichier JSON et le lire

with open("data/rdu-weather-history.json", "r") as file:
    data = json.load(file)

#définit une route API avec FastAPI
@app.post("/read_json")

@app.get("/data")
async def get_data(dated: str = None, datef: str = None):

    """
    Cette route permet de consulter les données en options avec filtrage par date.
    Args:
        dated (str, optional): Date de début de filtrage.
        datef (str, optional): Date de fin de filtrage.

    Returns:
        dict: Un dictionnaire JSON contenant les données filtrées ( ou tout les données si aucun filtre n'est spécifié).
    """
    filtered_data = data

    if dated:
        filtered_data = [item for item in filtered_data if item.get("date") >= dated]

    if datef:
        filtered_data = [item for item in filtered_data if item.get('date') <= datef]

        return {"message" : f"Il y'a {len(filtered_data)} releves entre le {dated} et le {datef}", "date": filtered_data}

    else:
        return {"date": data}


