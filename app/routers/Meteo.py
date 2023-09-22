from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..data import crud, schemas
from ..data.db import get_db

router = APIRouter()


@router.post("/createMeteo/", response_model=schemas.Meteo)
def create_meteo(meteo: schemas.MeteoCreate, db: Session = Depends(get_db)):
    """
     Créer des météos dans la base de données.
     
     Args:
     	 meteo: A: classe: ` schemes. météo Créer ` objet.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Une nouvelle classe créée: classe: ` météo. modèles. objet météorite
    """
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo.date)
    if db_meteo:
        raise HTTPException(status_code=409, detail="Date already registered")
    return crud.create_meteo(db=db, meteo=meteo, city_id=meteo.id_city)


@router.get("/getMeteos/", response_model=list[schemas.Meteo])
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


@router.get("/getMeteo/{meteo_date}", response_model=schemas.Meteo)
def read_meteo(meteo_date: str, db: Session = Depends(get_db)):
    """
     Voir météo par date
     
     Args:
     	 meteo_date: date de la météo à lire
     	 db: base de données à lire (par défaut: get_db)
     
     Returns: 
     	 avec des données de met
    """
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo_date)
    if db_meteo is None:
        raise HTTPException(status_code=404, detail="Meteo not found")
    return db_meteo

@router.put("/updateMeteo/{meteo_date}", response_model=schemas.Meteo)
def update_meteo(meteo_date: str, meteo_update: schemas.MeteoUpdate, db: Session = Depends(get_db)):
    """
     Météo mise à jour dans la base de données.
     
     Args:
     	 meteo_date: Date de mise à jour du météorologue.
     	 meteo_update: MeteoUpdate objet avec de nouvelles valeurs.
     	 db: Connexion de base de données à utiliser.
     
     Returns: 
     	 Retour à l' objet météo mis à jour
    """
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo_date)
    if db_meteo is None:
        raise HTTPException(status_code=404, detail="Meteo not found")

    # Mettez à jour les champs nécessaires de db_meteo à partir de meteo_update
    db_meteo.date = meteo_update.date
    db_meteo.tmin = meteo_update.tmin
    db_meteo.tmax = meteo_update.tmax
    db_meteo.prcp = meteo_update.prcp
    db_meteo.snow = meteo_update.snow
    db_meteo.snowd = meteo_update.snowd
    db_meteo.awnd = meteo_update.awnd
    db_meteo.id_city = meteo_update.id_city

    db.commit()
    db.refresh(db_meteo)
    return db_meteo

@router.delete("/deleteData", response_model=list[schemas.Meteo])
def delete_data(meteo_date: str, db: Session = Depends(get_db)):
    """
     Supprimer les données associées à une météorologie
     
     Args:
     	 meteo_date: date des données à supprimer
     	 db: base de données à utiliser pour la suppression
     
     Returns: 
     	 d'une valeur de
    """
    db_meteo = crud.delete_data(db, meteo_date=meteo_date)
    return db_meteo
