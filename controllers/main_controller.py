import pandas as pd
import time
import os

from models.chargement import Chargement
from models.nettoyage import Nettoyage
from models.rapprochement import Rapprochement
from models.comparaison import Comparaison
from models.synthese import Synthese
from models.panier import Panier
from models.historique import Historique

from views.produit_view import ProduitView
from views.menu_view import MenuView
from views.comparatif_view import ComparatifView
from views.synthese_view import SyntheseView
from views.panier_view import PanierView
from views.historique_view import HistoriqueView


class MainController:

    def __init__(self):

        # Initialisation des modèles
        self.chargement = Chargement()
        self.nettoyage = Nettoyage()
        self.rapprochement = Rapprochement()
        self.comparaison = Comparaison()
        self.synthese = Synthese()
        self.panier = Panier()
        self.historique = Historique()

        # Initialisation des vues
        self.menu_view = MenuView()
        self.produit_view = ProduitView()
        self.comparatif_view = ComparatifView()
        self.synthese_view = SyntheseView()
        self.panier_view = PanierView()
        self.historique_view = HistoriqueView()

        # Stockage des données
        self.donnees = None
        self.donnees_nettoyees = False

        self.comparatif = None
        self.resultat_synthese = None
        self.resultat_panier = None
        self.resultat_historique = None



    def charger_donnees(self):

        debut = time.perf_counter()

        try:
            self.donnees = self.chargement.charger_tout()

            fin = time.perf_counter()

            self.donnees_nettoyees = False
            self.comparatif = None

            print("\nLes cinq fichiers ont été chargés.")
            print("Temps de chargement :", fin - debut, "secondes")

        except Exception as erreur:
            print("Erreur lors du chargement :", erreur)


    def nettoyer_donnees(self):

        if self.donnees is None:
            print("Veuillez d'abord charger les données.")
            return

        if self.donnees_nettoyees:
            print("Les données sont déjà nettoyées.")
            return

        try:
            marche, baobab, comptoir, catalogue, historique = self.donnees

            marche = self.nettoyage.nettoyer_marche(marche)

            baobab = self.nettoyage.nettoyer_baobab(baobab)

            comptoir = self.nettoyage.nettoyer_comptoir(comptoir)

            self.donnees = (
                marche,
                baobab,
                comptoir,
                catalogue,
                historique
            )

            self.donnees_nettoyees = True

            print("\nNettoyage terminé avec succès.")

        except Exception as erreur:
            print("Erreur pendant le nettoyage :", erreur)

    def preparer_donnees_rapprochees(self):

        if self.donnees is None:
            print("Veuillez d'abord charger les données.")
            return None

        if not self.donnees_nettoyees:
            print("Veuillez d'abord nettoyer les données.")
            return None

        marche, baobab, comptoir, catalogue, historique = self.donnees

        toutes_donnees = pd.concat(
            [marche, baobab, comptoir],
            ignore_index=True
        )

        donnees_rapprochees = self.rapprochement.rapprocher(
            toutes_donnees,
            catalogue
        )

        return pd.DataFrame(donnees_rapprochees)

    def comparer_prix(self):

        donnees = self.preparer_donnees_rapprochees()

        if donnees is None or donnees.empty:
            print("Aucune donnée disponible pour la comparaison.")
            return

        self.comparatif = self.comparaison.comparer(donnees)

        self.comparatif_view.afficher(self.comparatif)


    def afficher_synthese(self):

        if self.comparatif is None:
            print("Veuillez d'abord comparer les prix.")
            return

        self.resultat_synthese = self.synthese.calculer(
            self.comparatif
        )

        self.synthese_view.afficher(
            self.resultat_synthese
        )



    def calculer_panier(self):

        donnees = self.preparer_donnees_rapprochees()

        if donnees is None or donnees.empty:
            print("Aucune donnée disponible pour le panier.")
            return

        self.resultat_panier = self.panier.calculer(
            donnees
        )

        self.panier_view.afficher(
            self.resultat_panier
        )



    def analyser_historique(self):

        if self.donnees is None:
            print("Veuillez d'abord charger les données.")
            return

        historique = self.donnees[4]

        debut = time.perf_counter()

        try:
            self.resultat_historique = self.historique.analyser(
                historique
            )

            fin = time.perf_counter()

            print("\nTemps d'analyse :", fin - debut, "secondes")

            self.historique_view.afficher(
                self.resultat_historique
            )

        except Exception as erreur:
            print("Erreur pendant l'analyse :", erreur)



    def exporter(self):

        if self.comparatif is None:
            print("Aucun comparatif à exporter.")
            return

        try:
            os.makedirs("resultats", exist_ok=True)

            self.comparatif.to_csv(
                "resultats/comparatif_prix.csv",
                index=False,
                encoding="utf-8-sig"
            )

            print("Exportation terminée avec succès.")

        except Exception as erreur:
            print("Erreur pendant l'exportation :", erreur)



    def afficher_catalogue(self):

        if self.donnees is None:
            print("Veuillez d'abord charger les données.")
            return

        catalogue = self.donnees[3]

        self.produit_view.afficher_catalogue(catalogue)



    def rechercher_produit(self):

        if self.donnees is None:
            print("Veuillez d'abord charger les données.")
            return

        catalogue = self.donnees[3]

        self.produit_view.rechercher_produit(catalogue)



    def comparer_selection(self):

        donnees = self.preparer_donnees_rapprochees()

        if donnees is None or donnees.empty:
            print("Aucun produit disponible.")
            return

        catalogue = self.donnees[3]

        identifiants = self.produit_view.selectionner_produits(
            catalogue
        )

        if not identifiants:
            print("Aucun produit valide sélectionné.")
            return

        selection = donnees[
            donnees["produit_id"].astype(str).isin(identifiants)
        ]

        if selection.empty:
            print("Aucune donnée disponible pour cette sélection.")
            return

        resultat = self.comparaison.comparer(selection)

        self.comparatif_view.afficher(resultat)



    def executer(self):

        while True:

            choix = self.menu_view.afficher_menu()

            if choix == "1":
                self.charger_donnees()

            elif choix == "2":
                self.nettoyer_donnees()

            elif choix == "3":
                self.afficher_catalogue()

            elif choix == "4":
                self.comparer_prix()

            elif choix == "5":
                self.rechercher_produit()

            elif choix == "6":
                self.comparer_selection()

            elif choix == "7":
                self.afficher_synthese()

            elif choix == "8":
                self.calculer_panier()

            elif choix == "9":
                self.analyser_historique()

            elif choix == "10":
                self.exporter()

            elif choix == "11":
                print("\nFermeture du programme. Merci !")
                break

            else:
                print("Choix invalide. Veuillez réessayer.")