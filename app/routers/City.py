from fastapi import APIRouter
from fastapi import Depends, HTTPException
from ..main import get_db
from sqlalchemy.orm import Session

from ..data import crud, models
from ..data import schemas

router = APIRouter()

@router.post("/createCity/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_city(db=db, city=city, country_id=city.id_country)


@router.get("/getCities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@router.get("/getCity/{city_name}", response_model=schemas.City)
def read_city(city_name: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_city


# ...

@router.put("/updateCities/{city_name}", response_model=schemas.City)
def update_city(city_name: str, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city_update.name

    db.commit()
    db.refresh(db_city)
    return db_city

@router.delete("/deleteCity", response_model=list[schemas.City])
def delete_cities(city_name: str, db: Session = Depends(get_db)):
    db_city = crud.delete_city(db, city_name=city_name)
    return db_city