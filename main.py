from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from data import crud, models, schemas
from data.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
import json
from fastapi import FastAPI
from component.reader import get_data, get_date_data, get_precipitation, get_temperature_range
from component.new import create_item

app = FastAPI()


# Dependency
def get_db():
    """
     Retourner une instance locale de session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/countries/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """
     Créer un pays dans le CRUD.
     
     Args:
     	 country: Un pays à créer.
     	 db: Connexion à base de données à utiliser.
     
     Returns: 
     	 Réponse objet avec code de statut et
    """
    db_country = crud.get_country_by_name(db, name=country.name)
    if db_country:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_country(db=db, country=country)


@app.get("/countries/", response_model=list[schemas.Country])
def read_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
     Lire les pays à partir de la base de données dépendante
     
     Args:
     	 skip: nombre de dossiers à ignorer
     	 limit: nombre maximum d'enregistrements à lire
     	 db: connexion à la base de données à utiliser pour la lecture
     
     Returns: 
     	 Liste des pays de la Communauté
    """
    countries = crud.get_countries(db, skip=skip, limit=limit)
    return countries


@app.get("/countries/{country_id}", response_model=schemas.Country)
def read_country(country_id: int, db: Session = Depends(get_db)):
    """
     Lire un pays dans la base de données
     
     Args:
     	 country_id: Identification du pays à lire
     	 db: connexion à la base de données à utiliser.
     
     Returns: 
     	 d'indiquer avec les informations relatives au pays ou
    """
    db_country = crud.get_country(db, user_id=country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_country


@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """
     Créez une ville en CRUD.
     
     Args:
     	 city: Une ville à créer.
     	 db: Connexion à base de données à utiliser.
     
     Returns: 
     	 réponse JSON avec des informations sur la ville
    """
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_city(db=db, city=city, country_id=city.id_country)


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
     Lisez les villes dans la base de données.
     
     Args:
     	 skip: Le nombre de disques à ignorer.
     	 limit: Le nombre maximal de disques à lire.
     	 db: Base de données à utiliser pour la lecture.
     
     Returns: 
     	 Liste de dictionnaires avec les touches " id " et " name "
    """
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@app.get("/cities/{city_id}", response_model=schemas.City)
def read_city(city_id: int, db: Session = Depends(get_db)):
    """
     Lisez une ville et retournez-la
     
     Args:
     	 city_id: id de la ville à lire
     	 db: db objet à utiliser pour la lecture
     
     Returns: 
     	 dicté de la ville ou 404 si ce n'est pas le cas
    """
    db_city = crud.get_city(db, user_id=city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_city

@app.post("/cities/{country_id}/cities/", response_model=schemas.City)
def create_country_for_city(
    city_id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)
):
    """
     Créer un pays pour une ville.
     
     Args:
     	 city_id: Identification de la ville à créer
     	 country: Objet contenant des informations sur la ville Pays
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 dict avec clés: id (int) nom (str)
    """
    return crud.create_city(db=db, country_id=country, city_id=city_id)


@app.post("/meteos/", response_model=schemas.Meteo)
def create_meteo(meteo: schemas.MeteoCreate, db: Session = Depends(get_db)):
    """
     Créer des météos dans la base de données.
     
     Args:
     	 meteo: A: classe: ` schemes. météo Créer ` objet.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Une nouvelle classe créée: classe: ` météo. modèles. objet météorite
    """
    db_meteo = crud.get_meteo_by_date(db, date=meteo.date)
    if db_meteo:
        raise HTTPException(status_code=400, detail="Date already registered")
    return crud.create_meteo(db=db, meteo=meteo, city_id=meteo.id_city)


@app.get("/meteos/", response_model=list[schemas.Meteo])
def read_meteos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
     Lisez les météos de la base de données.
     
     Args:
     	 skip: nombre de dossiers à ignorer
     	 limit: nombre maximum d'enregistrements à lire
     	 db: base de données à lire.
     
     Returns: 
     	 Liste des classes: ` marshmallow. modèles. Meta `
    """
    meteos = crud.get_meteos(db, skip=skip, limit=limit)
    return meteos


@app.get("/meteos/{meteo_id}", response_model=schemas.Meteo)
def read_meteo(meteo_id: int, db: Session = Depends(get_db)):
    """
     Lisez météo par id.
     
     Args:
     	 meteo_id: id du météo à lire
     	 db: db objet à utiliser pour la lecture
     
     Returns: 
     	 le dict avec les données de la
    """
    db_meteo = crud.get_meteo(db, meteo_id=meteo_id)
    if db_meteo is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_meteo


@app.post("/meteos/{meteo_id}/cities/", response_model=schemas.City)
def create_city_for_meteo(
    meteo_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)
):
    """
     Créer une ville pour une météo.
     
     Args:
     	 meteo_id: Identification du météorologue pour créer la ville pour
     	 city: Objet de la ville à créer.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 dicter avec les clés : id: ID de la ville créée
    """
    return crud.create_meteo_city(db=db, city=city, meteo_id=meteo_id)



