from faker import Faker
import random
import csv

fake = Faker()

# Liste des types de travail
types_travail = [
    "Taille de la vigne", 
    "Palissage", 
    "Traitements phytosanitaires", 
    "Désherbage", 
    "Fertilisation", 
    "Irrigation",
    "Récolte (Vendange)", 
    "Pressurage des raisins",
    "Entretien des équipements agricoles",
    "Aménagement du sol",
    "Surveillance de la santé des plantes",
    "Équilibrage du feuillage",
    "Préparation de la vigne pour l'hiver",
    "Travaux de plantation",
    "Autre"
]

# Création du fichier CSV avec les colonnes spécifiées
with open("travaux.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["id", "type_travail", "duree", "ouvrier_id", "date_travail"])

    for i in range(100):
        # Simuler un ouvrier (id unique pour chaque ouvrier)
        ouvrier_id = random.randint(1, 20)  # Exemple d'ouvriers, ici 20 ouvriers différents

        # Écrire une ligne dans le fichier CSV
        writer.writerow([
            i + 1,  # ID (clé primaire, auto-incrémentée)
            random.choice(types_travail),  # Type de travail choisi parmi la liste
            random.randint(1, 8),  # Durée du travail (en heures)
            ouvrier_id,  # Ouvrier ID (clé étrangère)
            fake.date_between(start_date="-1y", end_date="today")  # Date du travail
        ])
