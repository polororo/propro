import sqlite3
import os
import logging

# Configuration du logging
logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG,
                   format='[%(asctime)s] %(levelname)s — %(message)s',
                   datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger(__name__)

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialise le chemin de la base de données"""
        self.db_path = os.path.join(os.path.dirname(__file__), "database.db")
        logger.info("Gestionnaire de base de données initialisé")
    
    def get_connection(self):
        """Établit une connexion à la base de données"""
        try:
            connection = sqlite3.connect(self.db_path)
            connection.row_factory = sqlite3.Row  # Pour avoir les résultats sous forme de dictionnaire
            return connection
        except Exception as e:
            logger.error(f"Erreur de connexion à la base de données : {str(e)}")
            raise

# Instance globale du gestionnaire de base de données
db_manager = DatabaseManager() 