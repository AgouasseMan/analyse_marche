import pandas as pd
import json

class Chargement:
    def charger_csv(self):
        donnees = pd.read_csv("data/marche_lagune.csv", sep = ";")
        return donnees

    def charger_json(self):
        with open("data/marche_lagune.json", "r", encoding= "utf-8") as fichier:
            donnees = json.load(fichier)

            articles = donnees["items"]
            return articles

    def charger_excel(self):
        donnees = pd.read_excel("data/comptoir_ivoire.xlsx", sheet_name = "Tarifs octobre 2026"
                                , header = 2)
        return donnees

    def charger_catalogue(self):
        donnees = pd.read_excel("data/cataloque_reference.csv", sep= ";")
        return donnees

    def charger_historique(self):
        donnees = pd.read_excel("data/historique.csv")
        return donnees

    def charger_tout(self):
        marche = self.charger_csv()
        baobab = self.charger_json()
        comptoir = self.charger_json()
        catalogue = self.charger_catalogue()
        historique = self.charger_historique()

        return marche, baobab, comptoir, catalogue, historique

