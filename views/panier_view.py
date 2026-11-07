class PanierView:

    def afficher(self, resultats):

        magasins, optimise = resultats

        print("\n========== CALCUL DU PANIER ==========")

        for magasin, total in magasins.items():

            if total is None:
                print(magasin, ": Panier incomplet")
            else:
                print(magasin, ":", total, "FCFA")

        print("\nPanier optimisé :", optimise, "FCFA")