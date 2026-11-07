import logging


class Journal:

    logging.basicConfig(
        filename="resultats/journal_nettoyage.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    @staticmethod
    def enregistrer(message):
        logging.warning(message)