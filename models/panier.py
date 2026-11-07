class Panier:

    def __init__(self):

        self.articles = {
            "P04": 1,
            "P12": 1,
            "P14": 2,
            "P15": 1,
            "P28": 1
        }

    def calculer(self, donnees):

        resultats = {}

        for magasin in donnees["magasin"].unique():

            total = 0
            complet = True

            for produit_id, quantite in self.articles.items():

                produit = donnees[
                    (donnees["produit_id"] == produit_id) &
                    (donnees["magasin"] == magasin)
                ]

                if produit.empty:
                    complet = False
                    break

                prix = produit.iloc[0]["prix"]

                total += prix * quantite

            resultats[magasin] = total if complet else None

        total_optimise = 0

        for produit_id, quantite in self.articles.items():

            produit = donnees[
                donnees["produit_id"] == produit_id
            ]

            if produit.empty:
                return resultats, None

            prix_min = produit["prix"].min()

            total_optimise += prix_min * quantite

        return resultats, total_optimise