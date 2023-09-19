from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# Définissez le modèle de données DonneesJSON avec des valeurs par défaut
class DonneesJSON(BaseModel):
    date: datetime = datetime(2018, 10, 8)
    tmin: int
    tmax: int
    prcp: float
    snow: int
    snwd: int
    awnd: int

# Endpoint pour ajouter des données JSON
@app.post("/ajouter_donnees/")
async def ajouter_donnees(donnees: DonneesJSON):
    # Vous pouvez accéder aux données JSON ici
    date = donnees.date
    tmin = donnees.tmin
    tmax = donnees.tmax
    prcp = donnees.prcp
    snow = donnees.snow
    snwd = donnees.snwd
    awnd = donnees.awnd

    # Faites ce que vous voulez avec ces données

    return {"message": "Données ajoutées avec succès", "donnees_recues": {"date": date, "tmin": tmin, "tmax": tmax, "prcp": prcp, "snow": snow, "snwd": snwd, "awnd": awnd}}




"""

donnée à créer 

{
      "date": "2017-10-21",
      "tmin": 48,
      "tmax": 79,
      "prcp": 0,
      "snow": 0,
      "snwd": 0,
      "awnd": 2.01
    },"""