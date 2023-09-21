from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Modèle de données pour un pays
class Pays(BaseModel):
    nom: str
    population: int

# Configuration de la connexion à la base de données
db = mysql.connector.connect(
    host="localhost",
    user="votre_utilisateur",
    password="votre_mot_de_passe",
    database="votre_base_de_donnees"
)

@app.post("/ajouter_pays/")
async def ajouter_pays(pays: Pays):
    # Récupérez les données du modèle Pays
    nom = pays.nom
    population = pays.population

    # Utilisez la connexion à la base de données pour ajouter le pays
    cursor = db.cursor()
    cursor.execute("INSERT INTO pays (nom, population) VALUES (%s, %s)", (nom, population))
    db.commit()

    # Fermez le curseur et renvoyez une réponse
    cursor.close()

    return {"message": "Pays ajouté avec succès", "pays_ajouté": {"nom": nom, "population": population}}
