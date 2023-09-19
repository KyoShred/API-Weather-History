from fastapi import FastAPI
from component.data import load_data
from component.data import write_data
from component.data import write_data
from component.reader import get_data
from component.new import create_item

app = FastAPI()


@app.get("/data/date")
def get_date():
    return get_data(load_data())


@app.get("/data/int")
def get_date_filter(dated: str = None, datef: str = None):
    return get_date_data(load_data(), dated, datef)


@app.get("/data/prcp")
def get_precipitation(prcp: float):
    return get_precipitation(load_data(), prcp)


# Définition de la route POST /items
@app.post("/items")
def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float,
                awnd: float):  # Ajout d'une donnée métérologique

    return create_item(write_data(), date, tmin, tmax, prcp, snow, snwd, awnd)
