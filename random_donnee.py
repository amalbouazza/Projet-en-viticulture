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

def generate_random_name():
    # Générer un prénom et un nom aléatoires
    first_names = ['Jean', 'Pierre', 'Marie', 'Paul', 'Lucie', 'Alice', 'Michel', 'David', 'Nathalie', 'Thierry']
    last_names = ['Dupont', 'Martin', 'Bernard', 'Lemoine', 'Robert', 'Leclerc', 'Durand', 'Lefevre', 'Faure', 'Moreau']
    return random.choice(last_names), random.choice(first_names)

def insert_ouvriers(num_entries):
    connection = create_connection()
    cursor = connection.cursor()

    for _ in range(num_entries):
        nom, prenom = generate_random_name()
        cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))

    connection.commit()  # Confirmer les changements
    cursor.close()
    connection.close()

# Insérer 100 ouvriers
insert_ouvriers(100)
