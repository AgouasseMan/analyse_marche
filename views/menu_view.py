class MenuView:

    def afficher_menu(self):

        print("\n================================================")
        print("          ANALYSE COMPARATIVE DE MARCHE")
        print("================================================")

        print("1. Charger les données")
        print("2. Nettoyer les données")
        print("3. Afficher le catalogue des produits")
        print("4. Comparer tous les produits")
        print("5. Rechercher un produit")
        print("6. Comparer les produits sélectionnés")
        print("7. Afficher la synthèse")
        print("8. Calculer le panier")
        print("9. Analyser l'historique des prix")
        print("10. Exporter les résultats")
        print("11. Quitter")

        print("================================================")

        choix = input("Votre choix : ")

        return choix