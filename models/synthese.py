class Synthese:

    def calculer(self, comparatif):

        if comparatif.empty:
            return None

        statistiques = comparatif.groupby("magasin").agg(
            nombre_fois_moins_cher=(
                "magasin_moins_cher",
                lambda x: (x == x.name).sum()
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