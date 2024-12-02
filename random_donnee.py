import mysql.connector
from faker import Faker
import random
from datetime import datetime, timedelta

# Configuration de la connexion MySQL
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="viticulture"
)
cursor = conn.cursor()

# Initialisation de Faker
fake = Faker()

# Générer et insérer des données pour la table `ouvriers`
def generate_ouvriers(n):
    for _ in range(n):
        nom = fake.last_name()
        prenom = fake.first_name()
        cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))
    conn.commit()
    print(f"{n} ouvriers insérés avec succès.")

# Générer et insérer des données pour la table `phytosanitaire`
def generate_phytosanitaire(n):
    for _ in range(n):
        maladie = fake.word()
        stade = random.choice(["Début", "Moyen", "Avancé"])
        methode = random.choice(["Biologique", "Chimique", "Mécanique"])
        observation = fake.sentence()
        ouvrier_id = random.randint(1, 15)  # Suppose qu'il y a 15 ouvriers dans la table `ouvriers`
        cursor.execute(
            "INSERT INTO phytosanitaire (maladie, stade, methode, observation, ouvrier_id) VALUES (%s, %s, %s, %s, %s)",
            (maladie, stade, methode, observation, ouvrier_id)
        )
    conn.commit()
    print(f"{n} enregistrements phytosanitaires insérés avec succès.")

# Générer et insérer des données pour la table `travaux`
def generate_travaux(n):
    for _ in range(n):
        type_travail = random.choice([
            "Taille de la vigne", "Palissage", "Irrigation", "Fertilisation", 
            "Récolte (Vendange)", "Pressurage des raisins", "Surveillance de la santé", 
            "Travaux de plantation", "Entretien des outils", "Traitements phytosanitaires"
        ])
        duree = round(random.uniform(1.0, 8.0), 2)  # Durée entre 1 et 8 heures
        ouvrier_id = random.randint(1, 15)  # Suppose qu'il y a 15 ouvriers dans la table `ouvriers`
        date_travail = fake.date_between(start_date="-2y", end_date="today")
        cursor.execute(
            "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
            (type_travail, duree, ouvrier_id, date_travail)
        )
    conn.commit()
    print(f"{n} enregistrements de travaux insérés avec succès.")

# Appel des fonctions pour générer des données
generate_ouvriers(10)           # Ajouter 10 ouvriers
generate_phytosanitaire(10)     # Ajouter 10 enregistrements phytosanitaires
generate_travaux(20)            # Ajouter 20 enregistrements de travaux

# Fermeture de la connexion
cursor.close()
conn.close()
