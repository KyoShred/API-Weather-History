import json
from fastapi import FastAPI
from component.reader import get_data, get_date_data, get_precipitation, get_temperature_range
from component.new import create_item

app = FastAPI()


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
# @app.post("/items")
# async def create_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float,
#                 awnd: float):  # Ajout d'une donnée métérologique

#     return create_item(date, tmin, tmax, prcp, snow, snwd, awnd)
