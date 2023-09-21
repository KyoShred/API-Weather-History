from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str

class Country(CountryBase):
    id: int

    class Config:
        orm_mode =True

class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    id_country: int
    pass

class CityUpdate(BaseModel):
    name: str

class City(CityBase):
    id: int
    id_country: int

    class Config:
        orm_mode =True

class MeteoBase(BaseModel):
    date: str
    tmin: int
    tmax: int
    prcp: float
    snow: float
    snowd: float
    awnd: float

class MeteoCreate(MeteoBase):
    id_city: int
    pass

class MeteoUpdate(BaseModel):
    date: str
    tmin: int
    tmax: int
    prcp: float
    snow: float
    snowd: float
    awnd: float

class Meteo(MeteoBase):
    id: int
    id_city: int

    class Config:
        orm_mode =True
