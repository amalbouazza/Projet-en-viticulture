import mysql.connector
from mysql.connector import Error

def create_connection():
    """Créer une connexion à la base de données MySQL."""
    try:
        connection = mysql.connector.connect(
            host="localhost",      # Si vous utilisez WAMP, généralement localhost ou 127.0.0.1
            user="root",           # L'utilisateur MySQL de votre serveur local (par défaut c'est "root")
            password="",           # Le mot de passe de l'utilisateur MySQL (par défaut vide pour WAMP)
            database="viticulture"  # Le nom de la base de données que vous souhaitez utiliser
        )
        if connection.is_connected():
            print("Connexion réussie à la base de données")
            return connection
    except Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None
