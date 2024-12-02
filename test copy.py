import random
import mysql.connector
from datetime import datetime

# Connexion à la base de données MySQL
def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",  # Adresse de votre serveur MySQL
        port="3306",        # Port de connexion
        database="viticulture",  # Remplacez par le nom de votre base de données
        user="root",              # Votre utilisateur MySQL
        password=""  # Ajoutez ici votre mot de passe MySQL
    )

# Liste des maladies, stades, et méthodes
maladies = ["Mildiou", "Oïdium", "Botrytis", "Fusariose", "Verticilliose", "Autre"]
stades = ["Début de développement", "Phase de propagation", "Phase de maturité", "Phase terminale"]
methodes = ["Traitement chimique", "Traitement biologique", "Mécanique", "Autre"]

# Insérer des données aléatoires dans la table phytosanitaire
def insert_operations(num_entries):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        # Générer des données aléatoires et insérer dans la base de données
        for _ in range(num_entries):
            maladie = random.choice(maladies)
            stade = random.choice(stades)
            methode = random.choice(methodes)
            observation = f"Observation pour {maladie} au stade {stade} avec méthode {methode}"
            ouvrier_id = random.randint(1, 30)  # ID ouvrier, en supposant que vous avez 30 ouvriers

            cursor.execute(
                "INSERT INTO phytosanitaire (maladie, stade, methode, observation, ouvrier_id) VALUES (%s, %s, %s, %s, %s)",
                (maladie, stade, methode, observation, ouvrier_id)
            )

        connection.commit()
        print(f"{num_entries} opérations phytosanitaires ajoutées avec succès.")

    except mysql.connector.Error as err:
        print(f"Erreur lors de l'insertion : {err}")
    finally:
        cursor.close()
        connection.close()

# Insérer 200 entrées
insert_operations(200)
