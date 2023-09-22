from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..data import crud, schemas
from ..data.db import get_db


router = APIRouter()

@router.post("/createCountry/{country_name}", response_model=schemas.Country)
def create_country(country_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):
    """
     Créer un pays dans la base de données.
     
     Args:
     	 country_name: Nom du pays à créer.
     	 country: Objet de pays à créer.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Retourne l'objet pays créé
    """
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country:
        raise HTTPException(status_code=400, detail="Country already registered")
    return crud.create_country(db=db, country=country)


@router.get("/getCountries/", response_model=list[schemas.Country])
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
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found")
    return countries


@router.get("/getCountry/{country_name}", response_model=schemas.Country)
def read_country(country_name: str, db: Session = Depends(get_db)):
    """
     Lire un pays dans la base de données
     
     Args:
     	 country_name: Nom du pays à lire
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Le dictionnaire avec les données de la
    """
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country



@router.put("/updateCountry/{country_name}", response_model=schemas.Country)
def update_country(country_name: str, country_update: schemas.CountryUpdate, db: Session = Depends(get_db)):
    """
     Mise à jour du nom d'un pays
     
     Args:
     	 country_name: Nom du pays à mettre à jour
     	 country_update: Objet CountryUpdate contenant le nom et d'autres données
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Un dicton contenant les informations actualisées
    """
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db_country.name = country_update.name

    db.commit()
    db.refresh(db_country)
    return db_country

@router.delete("/deleteCountry", response_model=list[schemas.Country])
def delete_countries(country_name: str, db: Session = Depends(get_db)):
    """
     Supprimer le pays de la base de données.
     
     Args:
     	 country_name: Nom du pays à supprimer
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Vrai si le pays a été supprimé
    """
    crud.delete_country(db, country_name=country_name)
