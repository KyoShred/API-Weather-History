"""
API FastAPI permettent de supprimer des dates

"""
from datetime import date


def delete_data(dated: str, datef: str):
    """
    supprimer des données en fonction d'une intervalle de dates spécifiée.

    Args:
        dated:date de début de l'intervalle (ex : 2017-01-01)
        datef: date de fin de l'intervalle (ex : 2022-02-18)

    Returns:
        dict : message affichant combien de données ont été supprimées.
    """
    deleted_count = 0

# éviter des problèmes de modification, en parcourant cette copie des données
    data_copy = data.copy()

    for item in data_copy:
        if dated <= item['date'] <= datef:
            date.remove(item)
            deleted_count += 1

        return {'message':f'{deleted_count} les données supprimer'}
