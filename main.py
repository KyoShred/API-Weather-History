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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/countries/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, name=country.name)
    if db_country:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_country(db=db, country=country)


@app.get("/countries/", response_model=list[schemas.Country])
def read_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = crud.get_countries(db, skip=skip, limit=limit)
    return countries


@app.get("/country/{country_name}", response_model=schemas.Country)
def read_country(country_name: str, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    else
        #retrieve all cities for this country
        db_city = crud.get_city_by_name(db, country_name=country_name)
        if db_city is None:
            raise HTTPException(status_code=404, detail="City not found")
        else:
            #retrieve all meteos for this city
            db_meteo = crud.get_meteo_by_date(db, country_name=country_name)
            if db_meteo is None:
                raise HTTPException(status_code=404, detail="Meteo not found")
            else:
                return db_country, db_city, db_meteo



@app.put("/countryUpdate/{country_name}", response_model=schemas.Country)
def update_country(country_name: str, country_update: schemas.CountryUpdate, db: Session = Depends(get_db)):
    db_country = crud.get_country_by_name(db, country_name=country_name)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")

    db_country.name = country_update.name

    db.commit()
    db.refresh(db_country)
    return db_country




@app.post("/cities/", response_model=schemas.City)
def create_city(city: schemas.CityCreate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, name=city.name)
    if db_city:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_city(db=db, city=city, country_id=city.id_country)


@app.get("/cities/", response_model=list[schemas.City])
def read_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db, skip=skip, limit=limit)
    return cities


@app.get("/city/{city_name}", response_model=schemas.City)
def read_city(city_name: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_city

@app.post("/cities/{country_id}/cities/", response_model=schemas.City)
def create_country_for_city(
    city_id: int, country: schemas.CountryCreate, db: Session = Depends(get_db)
):
    return crud.create_city(db=db, country_id=country, city_id=city_id)


# ...

@app.put("/cities/{city_name}", response_model=schemas.City)
def update_city(city_name: str, city_update: schemas.CityUpdate, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db, city_name=city_name)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    db_city.name = city_update.name

    db.commit()
    db.refresh(db_city)
    return db_city



@app.post("/meteos/", response_model=schemas.Meteo)
def create_meteo(meteo: schemas.MeteoCreate, db: Session = Depends(get_db)):
    db_meteo = crud.get_meteo_by_date(db, date=meteo.date)
    if db_meteo:
        raise HTTPException(status_code=400, detail="Date already registered")
    return crud.create_meteo(db=db, meteo=meteo, city_id=meteo.id_city)


@app.get("/meteos/", response_model=list[schemas.Meteo])
def read_meteos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    meteos = crud.get_meteos(db, skip=skip, limit=limit)
    return meteos


@app.get("/meteos/{meteo_date}", response_model=schemas.Meteo)
def read_meteo(meteo_date: str, db: Session = Depends(get_db)):
    db_meteo = crud.get_meteo_by_date(db, meteo_date=meteo_date)
    if db_meteo is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_meteo


@app.post("/meteos/{meteo_id}/cities/", response_model=schemas.City)
def create_city_for_meteo(
    meteo_id: int, city: schemas.CityCreate, db: Session = Depends(get_db)
):
    return crud.create_meteo_city(db=db, city=city, meteo_id=meteo_id)


@app.put("/meteos/{meteo_date}", response_model=schemas.Meteo)
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

    db.commit()
    db.refresh(db_meteo)
    return db_meteo




