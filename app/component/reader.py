
"""
  Cette fonction permet de consulter les données météorologiques en options avec filtrage par date.

  Args:
    data (dict): Dictionnaire JSON contenant les données météorologiques.
    dated (str, optional): Date de début de filtrage.
    datef (str, optional): Date de fin de filtrage.

  Returns:
    dict: Un dictionnaire JSON contenant les données météorologiques filtrées ( ou tout les données si aucun filtre n'est spécifié).

"""


def get_data(data):
    """
     Retourne les données à afficher
     
     Args:
     	 data: liste des relevés pour chaque classe
     
     Returns: 
     	 avec le message et la date
    """
    return {"message": f"Il y a {len(data)} releves", "date": data}


def get_date_data(data, dated: str = None, datef: str = None):
    """
    Filtrage et retour des données qui sont relevés à la date
    
    Args:
        data: liste des dicts qui contiennent des données
        dated: date de filtration si Aucun filtrage n' est effectué
        datef: date de filtration si Aucun filtrage n' est effectué
    
    Returns: 
        données filtrées avec date et
    """

    filtered_data = data

    if dated:
        filtered_data = [
            item for item in filtered_data if item.get("date") >= dated]

    if datef:
        filtered_data = [
            item for item in filtered_data if item.get('date') <= datef]

        return {"message": f"Il y'a {len(filtered_data)} releves entre le {dated} et le {datef}", "date": filtered_data}


def get_precipitation(data, prcp: float):
    """
     Filtre et retourner les précipitations.
     
     Args:
     	 data: Liste des données à filtrer
     	 prcp: Relevance minimale des éléments (0 à 1)
     
     Returns: 
     	 Un dictionnaire avec deux touches " message " et " date "
    """
    if prcp:
        filtered_data = [
            item for item in data if item.get('prcp') >= prcp]
        return {"message": f"Il y'a {len(filtered_data)} releves avec une precipitation superieur a {prcp}", "date": filtered_data}
