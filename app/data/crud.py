from sqlalchemy.orm import Session

from . import models, schemas

def get_country(db: Session, country_id: int):
    """
     Obtenez un pays par ID
     
     Args:
     	 db: Une session de base de données à utiliser
     	 country_id: Identification du pays à rechercher
     
     Returns: 
     	 Le pays ou Aucun
    """
    return db.query(models.Country).filter(models.Country.id == country_id).first()

def get_country_by_name(db:Session, country_name: str):
    """
     Trouvez un pays par nom.
     
     Args:
     	 db: La base de données à utiliser.
     	 country_name: Le nom du pays.
     
     Returns: 
     	 Le pays ou Aucun si on ne le trouve pas
    """
    return db.query(models.Country).filter(models.Country.name == country_name).first()

def get_countries(db: Session, skip: int =0, limit: int = 100):
    """
     Obtenez des pays de la base de données.
     
     Args:
     	 db: base de données à utiliser pour la requête
     	 skip: nombre de dossiers à ignorer
     	 limit: nombre de dossiers à retourner
     
     Returns: 
     	 Liste des classes: ` ~django. db. modèles. pays
    """
    return db.query(models.Country).offset(skip).limit(limit).all()

def create_country(db: Session, country: schemas.CountryCreate):
    """
     Créer un pays dans la base de données.
     
     Args:
     	 db: session DB à utiliser pour les opérations de base de données
     	 country: Objet de pays à créer
     
     Returns: 
     	 l'objet pays nouvellement créé
    """
    db_country = models.Country(name=country.name)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country

def get_city(db:Session, city_id: int):
    """
     Trouvez une ville par ID
     
     Args:
     	 db: Une session de base de données à utiliser
     	 city_id: Le numéro de l'identifiant
    """
    db.query(models.City).filter(models.City.id == city_id).first()

def get_city_by_name(db: Session, city_name: str):
    """
     Trouvez une ville par nom.
     
     Args:
     	 db: Une session de base de données à utiliser.
     	 city_name: Le nom de la ville à rechercher.
     
     Returns: 
     	 La ville si on la trouve Pas d'autre
    """
    return db.query(models.City).filter(models.City.name == city_name).first()

def get_city_by_country(db: Session, id_country: int):
    """
     Prends toutes les villes pour un pays
     
     Args:
     	 db: la base de données à consulter.
     	 id_country: l'identifiant du pays.
     
     Returns: 
     	 une liste de: classe: ` ~mediadrop. modèle. ville `
    """
    return db.query(models.City).filter(models.Country.id == id_country).all()

def get_cities(db: Session, skip: int =0, limit: int = 100):
    """
     Obtenez des villes de la base de données.
     
     Args:
     	 db: Une connexion de base de données à utiliser.
     	 skip: Le nombre de disques à ignorer.
     	 limit: Nombre de dossiers à retourner.
     
     Returns: 
     	 Une liste de: classe: ` ~mediadrop. modèle.
    """
    return db.query(models.City).offset(skip).limit(limit).all()

def create_city(db: Session, city: schemas.CityCreate, country_id: int):
    """
     Créer une ville dans la base de données.
     
     Args:
     	 db: La base de données à utiliser.
     	 city: La ville à créer.
     	 country_id: L'identité du pays où la ville a été créée.
     
     Returns: 
     	 La ville créée dans la base de données
    """
    db_city = models.City(name=city.name, id_country=country_id)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city

def get_meteo(db: Session, meteo_id: int):
    """
     Météo par ID.
     
     Args:
     	 db: connexion db à utiliser.
     	 meteo_id: l'identifiant de la météorite à récupérer.
     
     Returns: 
     	 : une classe: ` météo. modèles. météo ` objet
    """
    return db.query(models.Meteo).filter(models.Meteo.id == meteo_id).first()

def get_meteo_by_date(db: Session, meteo_date: str):
    """
     Prenez le météo à la date.
     
     Args:
     	 db: connexion de base de données à utiliser
     	 meteo_date: date de la météo à récupérer
     
     Returns: 
     	 Les modèles de type
    """
    return db.query(models.Meteo).filter(models.Meteo.date == meteo_date).first()

def get_meteos(db: Session, skip: int =0, limit: int = 100):
    """
     Obtenez des météos de la base de données.
     
     Args:
     	 db: Une connexion de base de données à utiliser
     	 skip: Nombre de rangées à sauter
     	 limit: Nombre de rangées à retourner
     
     Returns: 
     	 Une liste de: classe: ` ~mediadrop. modèle. météo. météo `
    """
    return db.query(models.Meteo).offset(skip).limit(limit).all()

def create_meteo(db: Session, meteo: schemas.MeteoCreate, city_id: int):
    """
     Créer météo et l'ajouter à la base de données
     
     Args:
     	 db: db à utiliser pour les opérations de base de données
     	 meteo: objet contenant des données pour créer des météos
     	 city_id: id de la ville à ajouter
     
     Returns: 
     	 objet météo nouvellement créé
    """
    db_meteo = models.Meteo(date=meteo.date, tmin=meteo.tmin, tmax=meteo.tmax, prcp=meteo.prcp, snow=meteo.snow, snowd=meteo.snowd, awnd=meteo.awnd, id_city=city_id)
    db.add(db_meteo)
    db.commit()
    db.refresh(db_meteo)
    return db_meteo


def delete_country(db: Session, country_name: str):
    """
     Supprimer un pays de la base de données
     
     Args:
     	 db: La base de données à utiliser.
     	 country_name: Le nom du pays à supprimer.
     
     Returns: 
     	 Vrai si le pays a été supprimé Faux autrement
    """
    db_country = db.query(models.Country).filter(models.Country.name == country_name).first()

    if db_country:
        db.delete(db_country)
        db.commit()
        return True
    else:
        return False

def delete_city(db: Session, city_name: str):
    """
     Supprimer une ville de la base de données.
     
     Args:
     	 db: La connexion de base de données à utiliser.
     	 city_name: Le nom de la ville à supprimer.
     
     Returns: 
     	 Vrai si la ville a été supprimée Faux sinon
    """
    db_city = db.query(models.City).filter(models.City.name == city_name).first()

    if db_city:
        db.delete(db_city)
        db.commit()
        return True
    else:
        return False


def delete_data(db: Session, meteo_date: str):
    """
     Supprimez les données de météorologies.
     
     Args:
     	 db: base de données à utiliser pour la suppression
     	 meteo_date: date des données à supprimer
     
     Returns: 
     	 Vrai si les données ont été supprimées Faux
    """
    db_data = db.query(models.Meteo).filter(models.Meteo.date == meteo_date).first()

    if db_data:
        db.delete(db_data)
        db.commit()
        return True
    else:
        return False
