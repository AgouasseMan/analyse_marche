class Synthese:

    def calculer(self, comparatif):

        if comparatif.empty:
            return None

        comparatif = comparatif.copy()

        comparatif["est_moins_cher"] = (
            comparatif["magasin"] == comparatif["magasin_moins_cher"]
        )

        statistiques = comparatif.groupby("magasin").agg(
            nombre_fois_moins_cher=(
                "est_moins_cher",
                "sum"
            ),
            ecart_moyen=(
                "ecart_pourcentage",
                "mean"
            )
        )

        top3 = (
            comparatif.groupby("produit_id")["ecart_fcfa"]
            .max()
            .sort_values(ascending=False)
            .head(3)
        )

        return statistiques, top3