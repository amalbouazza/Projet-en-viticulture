import random
import mysql.connector
from datetime import datetime, timedelta

# Remplacez les informations par les vôtres
def create_connection():
    return mysql.connector.connect(
        host="127.0.0.1",  # Adresse de votre serveur MySQL (localhost)
        port="3306",        # Port de connexion (3306 est par défaut pour MySQL)
        database="viticulture",  # Remplacez par le nom de votre base de données
        user="root",              # Remplacez par votre utilisateur MySQL
        password=""  # Ajoutez ici le mot de passe
    )

def generate_random_date(start_date="2024-12-01", end_date="2024-12-31"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).strftime('%Y-%m-%d')

def insert_travaux(num_entries):
    connection = create_connection()
    cursor = connection.cursor()

    types_travaux = [
        'Taille de la vigne', 'Palissage', 'Traitements phytosanitaires', 
        'Désherbage', 'Fertilisation', 'Irrigation', 'Récolte (Vendange)', 
        'Pressurage des raisins', 'Entretien des équipements agricoles', 
        'Aménagement du sol', 'Surveillance de la santé des plantes', 
        'Équilibrage du feuillage', 'Préparation de la vigne pour l\'hiver', 
        'Travaux de plantation', 'Autre'
    ]
    
    for _ in range(num_entries):
        type_travail = random.choice(types_travaux)
        duree = round(random.uniform(2, 8), 2)  # Durée aléatoire entre 2 et 8 heures
        ouvrier_id = random.randint(1, 30)  # Assurez-vous d'avoir des ouvriers avec ces IDs
        date_travail = generate_random_date()

        cursor.execute(
            "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
            (type_travail, duree, ouvrier_id, date_travail)
        )

    connection.commit()
    cursor.close()
    connection.close()

# Insérer 200 travaux
insert_travaux(200)
