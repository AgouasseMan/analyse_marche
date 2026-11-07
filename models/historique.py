import pandas as pd


class Historique:

    def analyser(self, donnees):

        donnees["date"] = pd.to_datetime(donnees["date"])

        black_friday = donnees[
            (donnees["date"] >= "2025-11-24") &
            (donnees["date"] <= "2025-11-30")
        ]

        moyenne_annee = donnees.groupby(
            ["source", "produit_id"]
        )["prix_fcfa"].mean()

        moyenne_black_friday = black_friday.groupby(
            ["source", "produit_id"]
        )["prix_fcfa"].mean()

        resultat = pd.concat(
            [
                moyenne_annee.rename("moyenne_annee"),
                moyenne_black_friday.rename("moyenne_black_friday")
            ],
            axis=1
        )

        resultat["difference"] = (
            resultat["moyenne_annee"] -
            resultat["moyenne_black_friday"]
        )

        return resultat