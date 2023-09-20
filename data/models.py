from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from .database import Base

class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    cities = relationship("Cities",  back_populates="country")

class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    id_country= Column(Integer, ForeignKey("countries.id"))
    name = Column(String, Unique=True, index=True)

    country = relationship("Country", back_populates="cities")
    meteo = relationship("Meteo", back_populates="city")

class Meteo(Base):
    __tablename__ = "meteo"
    id = Column(Integer, primary_key=True, index=True)
    id_city = Column(Integer, ForeignKey("cities.id"))
    date = Column(String)
    tmin = Column(Integer)
    tmax = Column(Integer)
    prcp = Column(Float)
    snow = Column(Float)
    snowd = Column(Float)
    awnd = Column(Float)

    city = relationship("City", back_populates="meteo")

