import pandas as pd


class Comparaison:

    def comparer(self, donnees):

        resultats = []

        for produit_id, groupe in donnees.groupby("produit_id"):

            if groupe["magasin"].nunique() < 2:
                continue

            prix_min = groupe["prix"].min()

            magasin_moins_cher = groupe.loc[
                groupe["prix"].idxmin(), "magasin"
            ]

            for _, ligne in groupe.iterrows():

                ecart = ligne["prix"] - prix_min

                pourcentage = (
                    (ecart / prix_min) * 100
                    if prix_min > 0 else 0
                )

                resultats.append({
                    "produit_id": produit_id,
                    "magasin": ligne["magasin"],
                    "prix": ligne["prix"],
                    "magasin_moins_cher": magasin_moins_cher,
                    "ecart_fcfa": ecart,
                    "ecart_pourcentage": pourcentage
                })

        return pd.DataFrame(resultats)