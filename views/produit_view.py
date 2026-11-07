class ProduitView:

    def afficher_catalogue(self, catalogue):

        print("\n========== CATALOGUE DES PRODUITS ==========\n")

        print(catalogue.to_string(index=False))

        print("\n============================================")

    def rechercher_produit(self, catalogue):

        recherche = input("\nEntrez le nom ou l'identifiant du produit : ")

        resultat = catalogue[
            catalogue["nom"].str.contains(
                recherche,
                case=False,
                na=False
            ) |
            catalogue["produit_id"].str.contains(
                recherche,
                case=False,
                na=False
            )
        ]

        if resultat.empty:
            print("Aucun produit trouvé.")
        else:
            print("\nRésultat de la recherche :")
            print(resultat.to_string(index=False))

    def selectionner_produits(self, catalogue):

        print("\nEntrez les identifiants des produits à comparer.")
        print("Séparez les identifiants par des virgules.")
        print("Exemple : P04, P12, P14")

        choix = input("\nVotre sélection : ")

        identifiants = [
            identifiant.strip().upper()
            for identifiant in choix.split(",")
            if identifiant.strip()
        ]

        identifiants_valides = catalogue["produit_id"].astype(str).tolist()

        selection = [
            identifiant
            for identifiant in identifiants
            if identifiant in identifiants_valides
        ]

        identifiants_invalides = [
            identifiant
            for identifiant in identifiants
            if identifiant not in identifiants_valides
        ]

        if identifiants_invalides:
            print("Identifiants inconnus :", identifiants_invalides)

        return list(dict.fromkeys(selection))