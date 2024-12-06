import sqlite3
import os

def create_database():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Création de la table users si elle n'existe pas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            status TEXT DEFAULT 'user',
            otp_secret TEXT
        )
        ''')

        # Création de la table catalogue si elle n'existe pas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS catalogue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            categorie TEXT NOT NULL,
            description TEXT NOT NULL
        )
        ''')
            
        conn.commit()
        print("Base de données initialisée avec succès!")
        
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()