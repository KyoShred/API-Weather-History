from sqlalchemy.orm import Session

from . import models, schemas

def get_country(db: Session, country_id: int):
    return db.query(models.Country).filter(models.Country.id == country_id).first()

def get_country_by_name(db:Session, name: str):
    return db.query(models.Country).filter(models.Country.name == name).first()

def get_countries(db: Session, skip: int =0, limit: int = 100):
    return db.query(models.Country).offset(skip).limit(limit).all()

def create_country(db: Session, country: schemas.CountryCreate, city_id: int):
    db_country = models.Country(name=country.name, city_id=city_id)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_city(db:Session, city_id: int):
    db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, name: str):
    return db.query(models.City).filter(models.City.name == name).first()

def get_cities(db: Session, skip: int =0, limit: int = 100):
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate, country_id: int):
    db_city = models.City(name=city.name, country_id=country_id)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_meteo(db: Session, meteo_id: int):
    return db.query(models.Meteo).filter(models.Meteo.id == meteo_id).first()

def get_meteo_by_date(db: Session, date: str):
    return db.query(models.Meteo).filter(models.Meteo.date == date).first()

def get_meteos(db: Session, skip: int =0, limit: int = 100):
    return db.query(models.Meteo).offset(skip).limit(limit).all()

def create_meteo(db: Session, meteo: schemas.MeteoCreate, city_id: int):
    db_meteo = models.Country(date=meteo.date, tmin=meteo.tmin, tmax=meteo.tmax, prcp=meteo.prcp, snow=meteo.snow, snowd=meteo.snowd, awnd=meteo.awmd, city_id=city_id)
    db.add(db_meteo)
    db.commit()
    db.refresh(db_meteo)
    return db_meteo

