from fastapi import Depends, FastAPI, HTTPException



from app.routers import City, Country, Meteo

app = FastAPI()

app.include_router(City.router)
app.include_router(Country.router)
app.include_router(Meteo.router)



@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}