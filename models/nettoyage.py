import pandas as pd
import re
from utils.journal import Journal


class Nettoyage:

    def nettoyer_prix(self, prix):

        if pd.isna(prix):
            return None

        prix = str(prix)
        prix = re.sub(r"[^0-9,\.]", "", prix)

        if not prix:
            return None

        if "," in prix and "." in prix:
            if prix.rfind(",") > prix.rfind("."):
                prix = prix.replace(".", "").replace(",", ".")
            else:
                prix = prix.replace(",", "")

        elif "," in prix:
            prix = prix.replace(",", ".")

        try:
            return float(prix)
        except ValueError:
            return None

    def nettoyer_nom(self, nom):

        if pd.isna(nom):
            return ""

        nom = str(nom).lower().strip()
        nom = re.sub(r"[^a-z0-9 ]", " ", nom)
        nom = re.sub(r"\s+", " ", nom)

        return nom

    def nettoyer_marche(self, donnees):

        resultats = []

        for _, ligne in donnees.iterrows():

            prix = self.nettoyer_prix(ligne["prix"])

            if prix is None:
                Journal.enregistrer("Prix invalide dans Marché Lagune")
                continue

            disponibilite = str(ligne["disponibilite"]).strip()

            if disponibilite.lower() == "rupture":
                continue

            resultats.append({
                "magasin": "Marché Lagune",
                "nom": ligne["designation"],
                "prix": prix,
                "disponibilite": disponibilite,
                "note": self.nettoyer_prix(ligne["note_clients"]),
                "nb_avis": ligne["nb_avis"]
            })

        return pd.DataFrame(resultats)

    def nettoyer_baobab(self, donnees):

        resultats = []

        for article in donnees:

            prix = self.nettoyer_prix(
                article["pricing"]["amount"]
            )

            livraison = self.nettoyer_prix(
                article["pricing"]["delivery_fee"]
            )

            stock = article["stock"]

            if prix is None:
                Journal.enregistrer("Prix invalide dans Baobab Shop")
                continue

            if livraison is None:
                livraison = 0

            if stock <= 0:
                continue

            resultats.append({
                "magasin": "Baobab Shop",
                "nom": article["title"],
                "prix": prix + livraison,
                "disponibilite": "En stock",
                "note": article["rating"]["average"],
                "nb_avis": article["rating"]["count"]
            })

        return pd.DataFrame(resultats)

    def nettoyer_comptoir(self, donnees):

        resultats = []

        for _, ligne in donnees.iterrows():

            prix = self.nettoyer_prix(
                ligne["Prix catalogue (FCFA)"]
            )

            remise = self.nettoyer_prix(
                ligne["Remise (%)"]
            )

            quantite = ligne["Quantité en rayon"]

            if prix is None:
                Journal.enregistrer("Prix invalide dans Comptoir Ivoire")
                continue

            if pd.isna(quantite) or quantite <= 0:
                continue

            if remise is None:
                remise = 0

            prix_final = prix * (1 - remise / 100)

            resultats.append({
                "magasin": "Comptoir Ivoire",
                "nom": ligne["Article"],
                "prix": prix_final,
                "disponibilite": "En stock",
                "note": None,
                "nb_avis": 0
            })

        return pd.DataFrame(resultats)