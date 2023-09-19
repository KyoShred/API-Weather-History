from fastapi import FastAPI
from component.data import load_data
from component.reader import get_data

from component.new import create_item
import json


app = FastAPI()


@app.get("/data")
async def get_date_data():
    return get_data(load_data())


@app.get("/data/{dated}-{datef}")
async def get_date_data(dated: str = None, datef: str = None):
    data = load_data()

    return get_data(data, dated, datef)

@app.get("/data/{prcp}")
async def get_precipitation(prcp: float):
    data = load_data()

    return get_precipitation(data, prcp)


# Définition de la route POST /items
@app.post("/items")

async def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float, awnd: float):   # Ajout d'une donnée métérologique

    return create_item(date, tmin, tmax, prcp, snow, snwd, awnd)
