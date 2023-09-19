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
@app.get("/data")
async def get_data(S_date: str = None, E_date: str = None):

    """
    Cette route permet de consulter les données en options avec filtrage par date.
    Args:
        S_date (str, optional): Date de début de filtrage.
        E_date (str, optional): Date de fin de filtrage.

    Returns:
        dict: Un dictionnaire JSON contenant les données filtrées ( ou tout les données si aucun filtre n'est spécifié).
    """
    filtered_data = data

    if S_date:
        filtered_data = [item for item in filtered_data if item.get("date") >= S_date]

    if E_date:
        filtered_data = [item for item in filtered_data if item.get('date') <= E_date]

        return {"date": filtered_data}





