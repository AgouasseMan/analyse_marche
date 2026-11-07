class SyntheseView:

    def afficher(self, resultats):

        if resultats is None:
            print("Aucune donnée disponible.")
            return

        statistiques, top3 = resultats

        print("\n SYNTHESE")

        print(statistiques)

        print("\nLES 3 PRODUITS LES PLUS INTERESSANTS A COMPARER")

        print(top3)