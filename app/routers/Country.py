from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..data import crud, schemas
from ..data.db import get_db


router = APIRouter()

@router.post("/createCountry/{country_name}", response_model=schemas.Country)
def create_country(country_name: str, country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country:
        raise HTTPException(status_code=400, detail="Country already registered")
    return crud.create_country(db=db, country=country)


@router.get("/getCountries/", response_model=list[schemas.Country])
def read_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = crud.get_countries(db, skip=skip, limit=limit)
    if not countries:
        raise HTTPException(status_code=404, detail="No countries found")
    return countries


@router.get("/getCountry/{country_name}", response_model=schemas.Country)
def read_country(country_name: str, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country



@router.put("/updateCountry/{country_name}", response_model=schemas.Country)
def update_country(country_name: str, country_update: schemas.CountryUpdate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db_country.name = country_update.name

    db.commit()
    db.refresh(db_country)
    return db_country

@router.delete("/deleteCountry", response_model=list[schemas.Country])
def delete_countries(country_name: str, db: Session = Depends(get_db)):
    crud.delete_country(db, country_name=country_name)
