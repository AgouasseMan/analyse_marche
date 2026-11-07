from dataclasses import dataclass

@dataclass
class Produit:
    produit_id: str
    nom : str
    categorie : str
    marque : str

