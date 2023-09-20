import json
from http.client import HTTPException

from fastapi import FastAPI
from component.data import load_data
from component.data import write_data
from component.reader import get_data


app = FastAPI()

data = load_data()


@app.get("/data")
def get_date():
    return get_data(load_data())


@app.get("/data_int")
def get_date_filter(dated: str = None, datef: str = None):
    return get_date(load_data(), dated, datef)


@app.get("/data_prcp")
def get_precipitation(prcp: float):
    return get_precipitation(load_data(), prcp)


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


class HTTPException:
    pass


@app.patch("/modify")
async def modify_item(date: str, tmin: int, tmax: int, prcp: float, snow: float, snwd: float,
                      awnd: float):
    donnee = 0
    found = False  # Utilisez cette variable pour indiquer si une correspondance a été trouvée
    for i in data:
        donnee +=1
        if i["date"] == date:
            found = True

    if found:
        print(f"modification possible à la donnée {donnee}")

    else:
        print(f"aucune donnée n'existe à la date {date}")

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