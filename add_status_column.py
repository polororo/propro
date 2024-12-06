import sqlite3
import os

def add_status_column():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'database.db')
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la colonne existe déjà
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        if not any(column[1] == 'status' for column in columns):
            # Ajouter la colonne status avec 'user' comme valeur par défaut
            cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'user'")
            
            # Mettre à jour le premier utilisateur comme admin
            cursor.execute("UPDATE users SET status = 'admin' WHERE rowid = 1")
            
        conn.commit()
        print("Colonne status ajoutée avec succès!")
        
    except sqlite3.Error as e:
        print(f"Une erreur est survenue : {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    add_status_column() 