from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

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

with open("data/rdu-weather-history.json", "r") as file:
    load_data = json.load(file)


# with open("data/rdu-weather-history.json", "w") as file:
#     json.dump(wdata, file, indent=4)


@app.get("/date")
def get_date():
    """Display all the data from the json file.

    Returns:
        dict: JSON data.
    """
    return get_data(load_data)


@app.get("/int")
def get_date_filter(dated: str = None, datef: str = None):
    """Display all date within the given range.

    Args:
        dated (str, required): starting date. Defaults to None.
        datef (str, required): ending date. Defaults to None.

    Returns:
        dict: A JSON dictionary and given date.

    """
    return get_date_data(load_data, dated, datef)


@app.get("/prcp")
async def get_precipitation_async(rain: float):
    """
    Retrieves precipitation data above a given value.

    Args:
        rain (float, required): The minimum precipitation value.

    Returns:
        dict: A JSON dictionary containing filtered precipitation data.

    """

    return get_precipitation(load_data, rain)


@app.get("/temp")
async def get_temperature(mintemp: float, maxtemp: float):
    """
    Retrieves temperature data within a given range.

    Args:
        mintemp (float): The minimum temperature value.
        maxtemp (float): The maximum temperature value.

    Returns:
        dict: A JSON dictionary containing the filtered temperature data.

    """

    return get_temperature_range(load_data, mintemp, maxtemp)


# Définition de la route POST /items
@app.post("/items")
async def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float,
                      awnd: float):  # Ajout d'une donnée métérologique

    new_entry = {
        "date": date,
        "tmin": tmin,
        "tmax": tmax,
        "prcp": prcp,
        "snow": snow,
        "snwd": snwd,
        "awnd": awnd
    }

    write_data(data).append(new_entry)
    return {"message": "Données ajoutées avec succès"}


@app.delete("/delete")
async def delete_item(date_compare: str):
    donnee = 0
    found = False  # Utilisez cette variable pour indiquer si une correspondance a été trouvée

    for i in data:
        donnee += 1
        if i["date"] == date_compare:
            print(f"élément trouvé à la donnée {donnee}")
            data.remove(i)
            with open("data/rdu-weather-history.json", "w") as file:
                json.dump(data, file, indent=4)

            print(f"élément supprimé")
            found = True  # Indiquez que vous avez trouvé une correspondance

    if found:
        return {"message": f"Donnée pour la date {date_compare} supprimée avec succès."}
    else:
        return {"message": f"Aucune donnée correspondant à la date {date_compare} n'a été trouvée."}




@app.put("/update/{date}")
async def update_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float, awnd: float):
    found = False  # Utilisez cette variable pour indiquer si une correspondance a été trouvée
    for i in data:
        if i["date"] == date:
            i["tmin"] = tmin
            i["tmax"] = tmax
            i["prcp"] = prcp
            i["snow"] = snow
            i["snwd"] = snwd
            i["awnd"] = awnd
            found = True

    if found:
        with open("data/rdu-weather-history.json", "w") as file:
            json.dump(data, file, indent=4)
        return {"message": f"Donnée pour la date {date} mise à jour avec succès."}
    else:
        raise HTTPException(status_code=404, detail=f"Aucune donnée correspondant à la date {date} n'a été trouvée.")
