from difflib import SequenceMatcher
import re


class Rapprochement:

    def normaliser(self, nom):

        nom = str(nom).lower()
        nom = re.sub(r"[^a-z0-9]", "", nom)

        return nom

    def rapprocher(self, donnees, catalogue):

        resultats = []

        for _, ligne in donnees.iterrows():

            nom = self.normaliser(ligne["nom"])

            meilleur_id = None
            meilleur_score = 0

            for _, produit in catalogue.iterrows():

                nom_reference = self.normaliser(produit["nom"])

                score = SequenceMatcher(
                    None,
                    nom,
                    nom_reference
                ).ratio()

                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_id = produit["produit_id"]

            if meilleur_score >= 0.70:

                ligne_resultat = ligne.to_dict()
                ligne_resultat["produit_id"] = meilleur_id

                resultats.append(ligne_resultat)

            else:
                print("Produit non reconnu :", ligne["nom"])

        return resultats