import sqlite3
import logging
import os

# Configuration du logging
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG,
                   format='[%(asctime)s] %(levelname)s — %(message)s',
                   datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

def add_otp_column():
    try:
        # Utilisation du chemin correct pour database.db
        db_path = os.path.join(os.path.dirname(__file__), "database.db")
        connection = sqlite3.connect(db_path)
        curseur = connection.cursor()
        
        # Création de la table si elle n'existe pas
        curseur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL PRIMARY KEY,
            password TEXT NOT NULL,
            status TEXT NOT NULL
        )
        """)
        
        # Ajout de la colonne otp_secret
        try:
            curseur.execute("ALTER TABLE users ADD COLUMN otp_secret TEXT")
            logger.info("Colonne otp_secret ajoutée avec succès à la table users")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                logger.warning("La colonne otp_secret existe déjà")
            else:
                raise
        
        connection.commit()
        
    except Exception as e:
        logger.error(f"Erreur inattendue : {str(e)}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    add_otp_column() 