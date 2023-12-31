from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.data import crud, schemas
from app.data.db import get_db

router = APIRouter()

@router.post("/createCity/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    """
     Créez une ville dans la base de données.
     
     Args:
     	 city: Une ville à créer.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 réponse JSON avec des informations sur la ville
    """
    db_city = crud.get_city_by_name(db, city_name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_city(db=db, city=city, country_id=city.id_country)


@router.get("/getCities/", response_model=list[schemas.City])
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


@router.get("/getCity/{city_name}", response_model=schemas.City)
def read_city(city_name: str, db: Session = Depends(get_db)):
    """
     Lisez une ville par son nom
     
     Args:
     	 city_name: Nom de la ville à lire
     	 db: Connexion de base de données à utiliser (par défaut get_db)
     
     Returns: 
     	 Objet de ville ou 404 si ce n'est pas le cas
    """
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_city

@router.get("/getCitiesByCountry/{country_name}", response_model=list[schemas.City])
def read_cities_by_country(country_name: str, db: Session = Depends(get_db)):
    """
     Lire les villes par pays
     
     Args:
     	 country_name: Nom du pays à rechercher
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Liste des classes: ` ~city_model.
    """
    cities = crud.get_cities_by_country_name(db, country_name=country_name)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found for this country")
    return cities
# ...

@router.put("/updateCities/{city_name}", response_model=schemas.City)
def update_city(city_name: str, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    """
     Mise à jour du nom d'une ville
     
     Args:
     	 city_name: Nom de la ville à mettre à jour
     	 city_update: Objet CityUpdate contenant le nom
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Objet de ville avec nom mis à jour
    """
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city_update.name

    db.commit()
    db.refresh(db_city)
    return db_city

@router.delete("/deleteCity", response_model=list[schemas.City])
def delete_cities(city_name: str, db: Session = Depends(get_db)):
    """
     Supprimer les villes en fonction du nom de la ville
     
     Args:
     	 city_name: Nom de la ville à supprimer
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Un dictionnaire des mots supprimés
    """
    db_city = crud.delete_city(db, city_name=city_name)
    return db_city