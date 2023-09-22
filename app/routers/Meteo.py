from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..data import crud, schemas
from ..data.db import get_db

router = APIRouter()


@router.post("/createMeteo/", response_model=schemas.Meteo)
def create_meteo(meteo: schemas.MeteoCreate, db: Session = Depends(get_db)):
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo.date)
    if db_meteo:
        raise HTTPException(status_code=409, detail="Date already registered")
    return crud.create_meteo(db=db, meteo=meteo, city_id=meteo.id_city)


@router.get("/getMeteos/", response_model=list[schemas.Meteo])
def read_meteos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meteos = crud.get_meteos(db, skip=skip, limit=limit)
    return meteos


@router.get("/getMeteo/{meteo_date}", response_model=schemas.Meteo)
def read_meteo(meteo_date: str, db: Session = Depends(get_db)):
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo_date)
    if db_meteo is None:
        raise HTTPException(status_code=404, detail="Meteo not found")
    return db_meteo

@router.get("/getMeteosByCity/{city_name}", response_model=list[schemas.Meteo])
def read_meteos_by_city(city_name: str, db: Session = Depends(get_db)):
    meteos = crud.get_meteos_by_city_name(db, city_name=city_name)
    if not meteos:
        raise HTTPException(status_code=404, detail="No meteos found for this city")
    return meteos

@router.put("/updateMeteo/{meteo_date}", response_model=schemas.Meteo)
def update_meteo(meteo_date: str, meteo_update: schemas.MeteoUpdate, db: Session = Depends(get_db)):
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
    db_meteo = crud.delete_data(db, meteo_date=meteo_date)
    return db_meteo
