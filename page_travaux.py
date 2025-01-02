from tkinter import Frame, Label, Entry, Button, messagebox
from tkinter import ttk, filedialog, scrolledtext
from tkcalendar import Calendar
import csv
from database import create_connection
import pickle
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

class PageTravaux(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=10, pady=10)
        self.configure(bg="#f4f4f4")

        # Titre
        title_label = Label(self, text="Gestion des Travaux", font=("Arial", 24, "bold"), bg="#f4f4f4", fg="#333333")
        title_label.pack(pady=20)

        # Frame pour organiser les champs
        form_frame = Frame(self, bg="#f4f4f4")
        form_frame.pack(pady=10)

        # Type de Travail et Durée sur la même ligne
        Label(form_frame, text="Type de Travail :", font=("Arial", 14), bg="#f4f4f4").grid(row=0, column=0, padx=(0, 20), pady=5)
        self.type_combobox = ttk.Combobox(form_frame, values=[ 
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
        ], font=("Arial", 12))
        self.type_combobox.grid(row=0, column=1, pady=5)

        Label(form_frame, text="Durée (heures) :", font=("Arial", 14), bg="#f4f4f4").grid(row=1, column=0, pady=5)
        self.duree_entry = Entry(form_frame, font=("Arial", 12), relief="solid", bd=1, width=30, bg="#ffffff")
        self.duree_entry.grid(row=1, column=1, pady=5)

        # Ouvrier et Date du travail sur la même ligne
        Label(form_frame, text="ID de l'Ouvrier :", font=("Arial", 14), bg="#f4f4f4").grid(row=2, column=0, pady=5)
        self.ouvrier_combobox = ttk.Combobox(form_frame, font=("Arial", 12))
        self.ouvrier_combobox.grid(row=2, column=1, pady=5)

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        Label(form_frame, text="Date du travail :", font=("Arial", 14), bg="#f4f4f4").grid(row=3, column=0, pady=5)
        self.calendrier = Calendar(form_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendrier.grid(row=3, column=1, pady=10)

        # Boutons personnalisés
        bouton_frame = Frame(self, bg="#f4f4f4")
        bouton_frame.pack(pady=(10, 5))

        bouton_ajouter = Button(bouton_frame, text="Ajouter Travail", command=self.ajouter_travail, font=("Arial", 12), bg="#4CAF50", fg="white", relief="raised", bd=2)
        bouton_ajouter.grid(row=0, column=0, padx=10)

        bouton_importer = Button(bouton_frame, text="Importer Travaux depuis Fichier", command=self.importer_travaux, font=("Arial", 12), bg="#008CBA", fg="white", relief="raised", bd=2)
        bouton_importer.grid(row=0, column=1, padx=10)

        # Bouton de prédiction
        bouton_predire = Button(bouton_frame, text="Prédire Type de Travail", command=self.predire_type_travail, font=("Arial", 12), bg="#FFC107", fg="white", relief="raised", bd=2)
        bouton_predire.grid(row=0, column=2, padx=10)

        # Bouton pour afficher les rapports
        bouton_rapport = Button(bouton_frame, text="Afficher Rapports", command=self.afficher_rapport, font=("Arial", 12), bg="#FF5722", fg="white", relief="raised", bd=2)
        bouton_rapport.grid(row=0, column=3, padx=10)

        # Table pour afficher les travaux
        self.tree = ttk.Treeview(self, columns=("ID", "Type", "Durée", "Ouvrier", "Date"), show="headings", height=8)
        self.tree.pack(pady=(20, 10))

        # Définir les colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type de Travail")
        self.tree.heading("Durée", text="Durée (heures)")
        self.tree.heading("Ouvrier", text="Ouvrier")
        self.tree.heading("Date", text="Date du Travail")

        # Remplir la table avec les travaux existants
        self.afficher_travaux()

    def remplir_liste_ouvriers(self):
        """Remplir la liste déroulante avec les ouvriers de la base de données."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom FROM ouvriers")
                ouvriers = cursor.fetchall()
                # Ajouter les ouvriers dans la combobox
                self.ouvrier_combobox['values'] = [f"{ouvrier[0]} - {ouvrier[1]}" for ouvrier in ouvriers]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des ouvriers : {str(e)}")
        finally:
            connection.close()

    def predire_type_travail(self):
        """Effectuer une prédiction du type de travail."""
        # Obtenez les données saisies par l'utilisateur
        duree = self.duree_entry.get()
        ouvrier_id = self.ouvrier_combobox.get()
        type_travail = self.type_combobox.get()  # Ajout du type de travail
        date_travail = self.calendrier.get_date()  # Ajout de la date du travail

        if not duree or not ouvrier_id or not type_travail or not date_travail:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs pour prédire.")
            return
        
        try:
            # Assurez-vous que la durée et l'ID de l'ouvrier sont des valeurs numériques valides
            duree = float(duree)  # Convertir la durée en float
            ouvrier_id = ouvrier_id.split(' - ')[0]  # Séparer l'ID du nom et prendre seulement l'ID
            ouvrier_id = float(ouvrier_id)  # Convertir l'ID en float

            # Convertir le type de travail et la date en valeurs numériques
            type_travail_num = self.convertir_type_travail_en_num(type_travail)
            date_travail_num = self.convertir_date_en_nombre(date_travail)

            # Charger le modèle
            with open('ml_models/ml_models/type_travail_model.pkl', 'rb') as model_file:
                model = pickle.load(model_file)

            # Préparer les données pour la prédiction (4 caractéristiques)
            input_data = np.array([[duree, ouvrier_id, type_travail_num, date_travail_num]])

            # Prédire
            prediction = model.predict(input_data)

            # Dictionnaire de correspondance entre l'index et le type de travail
            mapping = {
                0: "Taille de la vigne",
                1: "Palissage",
                2: "Traitements phytosanitaires",
                3: "Désherbage",
                4: "Fertilisation",
                5: "Irrigation",
                6: "Récolte (Vendange)",
                7: "Pressurage des raisins",
                8: "Entretien des équipements agricoles",
                9: "Aménagement du sol",
                10: "Surveillance de la santé des plantes",
                11: "Équilibrage du feuillage",
                12: "Préparation de la vigne pour l'hiver",
                13: "Travaux de plantation",
                14: "Autre"
            }

            # Récupérer le type de travail prédit
            predicted_type = mapping.get(prediction[0], "Inconnu")

            # Afficher le résultat
            messagebox.showinfo("Prédiction", f"Le type de travail prédit est : {predicted_type}")
            print(f"Prédiction réussie : Le type de travail prédit est {predicted_type}")

            # Enregistrer les résultats dans un fichier CSV
            with open('predictions.csv', mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([duree, ouvrier_id, predicted_type, date_travail])

        except ValueError:
            messagebox.showerror("Erreur", "La durée et l'ID de l'ouvrier doivent être des nombres valides.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la prédiction : {str(e)}")

    def afficher_travaux(self):
        """Afficher tous les travaux dans la table."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM travaux")
                travaux = cursor.fetchall()
                # Remplir la table avec les travaux
                for travail in travaux:
                    self.tree.insert("", "end", values=travail)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage des travaux : {str(e)}")
        finally:
            connection.close()

    def afficher_rapport(self):
        """Afficher un graphique basé sur les données du fichier CSV."""
        try:
            # Lire le fichier CSV contenant les travaux
            df = pd.read_csv('predictions.csv', names=["Durée", "ID_Ouvrier", "Type_Travail", "Date"])

            # Créer un graphique pour afficher la durée du travail par type de travail
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Grouper par type de travail et sommer les durées
            graphique_data = df.groupby("Type_Travail")["Durée"].sum().sort_values()

            # Créer un graphique à barres
            graphique_data.plot(kind='barh', ax=ax, color='skyblue')

            # Ajouter des labels et un titre
            ax.set_xlabel("Durée Totale (heures)")
            ax.set_ylabel("Type de Travail")
            ax.set_title("Durée Totale des Travaux par Type")

            # Afficher le graphique
            plt.tight_layout()
            plt.show()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {str(e)}")

    def importer_travaux(self):
        """Importer les travaux depuis un fichier CSV."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        # Ajouter les données dans la base de données
                        self.ajouter_travail(row)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'importation des travaux : {str(e)}")

    def ajouter_travail(self, travail_data):
        """Ajouter un travail dans la base de données."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)", travail_data)
                connection.commit()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout du travail : {str(e)}")
        finally:
            connection.close()

    def convertir_type_travail_en_num(self, type_travail):
        """Convertir le type de travail en valeur numérique."""
        mapping = {
            "Taille de la vigne": 0,
            "Palissage": 1,
            "Traitements phytosanitaires": 2,
            "Désherbage": 3,
            "Fertilisation": 4,
            "Irrigation": 5,
            "Récolte (Vendange)": 6,
            "Pressurage des raisins": 7,
            "Entretien des équipements agricoles": 8,
            "Aménagement du sol": 9,
            "Surveillance de la santé des plantes": 10,
            "Équilibrage du feuillage": 11,
            "Préparation de la vigne pour l'hiver": 12,
            "Travaux de plantation": 13,
            "Autre": 14
        }
        return mapping.get(type_travail, -1)

    def convertir_date_en_nombre(self, date_str):
        """Convertir une date (yyyy-mm-dd) en un nombre."""
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            return int(date_obj.strftime('%Y%m%d'))  # Exemple de conversion
        except ValueError:
            return 0  # Si la date est invalide
        

