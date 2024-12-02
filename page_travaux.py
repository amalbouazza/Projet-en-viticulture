from tkinter import Frame, Label, Entry, Button, messagebox
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import csv
from database import create_connection
import pickle
import numpy as np

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
        
        if not duree or not ouvrier_id:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs pour prédire.")
            return
        
        try:
            # Assurez-vous que la durée et l'ID de l'ouvrier sont des valeurs numériques valides
            duree = float(duree)  # Convertir la durée en float
            ouvrier_id = ouvrier_id.split(' - ')[0]  # Sépare l'ID du nom, et prend seulement l'ID
            ouvrier_id = float(ouvrier_id)  # Convertir l'ID en float

            print(f"Donnée de durée: {duree} heures")
            print(f"Donnée d'ouvrier ID: {ouvrier_id}")
            
            # Charger le modèle
            with open('ml_models/ml_models/type_travail_model.pkl', 'rb') as model_file:
                model = pickle.load(model_file)

            # Préparer les données pour la prédiction
            input_data = np.array([[duree, ouvrier_id]])  # Assurez-vous que c'est un tableau 2D

            # Prédire
            prediction = model.predict(input_data)

            # Afficher le résultat
            messagebox.showinfo("Prédiction", f"Le type de travail prédit est : {prediction[0]}")
            print(f"Prédiction réussie : Le type de travail prédit est {prediction[0]}")

        except ValueError as ve:
            messagebox.showerror("Erreur de Données", f"Erreur de conversion des données : {str(ve)}")
            print(f"Erreur de conversion des données : {str(ve)}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la prédiction : {str(e)}")
            print(f"Erreur lors de la prédiction : {str(e)}")

    def ajouter_travail(self):
        """Ajouter un travail dans la base de données."""
        type_travail = self.type_combobox.get()
        
        if type_travail == "Autre":
            type_travail = self.other_type_entry.get()

        duree = self.duree_entry.get()
        date_travail = self.calendrier.get_date()
        
        # Récupérer l'ID de l'ouvrier
        selection = self.ouvrier_combobox.get()
        if selection:
            ouvrier_id = selection.split(' - ')[0]
        else:
            ouvrier_id = None

        if type_travail and duree and ouvrier_id and date_travail:
            try:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
                        (type_travail, duree, ouvrier_id, date_travail)
                    )
                connection.commit()
                messagebox.showinfo("Succès", f"Travail '{type_travail}' ajouté avec succès")
                self.type_combobox.set('')
                self.duree_entry.delete(0, 'end')
                self.ouvrier_combobox.set('')
                self.calendrier.set_date('')
                self.afficher_travaux()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du travail : {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def afficher_travaux(self):
        """Afficher les travaux dans la table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, type_travail, duree, ouvrier_id, date_travail FROM travaux")
                travaux = cursor.fetchall()

                for travail in travaux:
                    self.tree.insert("", "end", values=travail)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des travaux : {str(e)}")
        finally:
            connection.close()

    def importer_travaux(self):
        """Importer les travaux depuis un fichier CSV."""
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if fichier:
            try:
                with open(fichier, newline='', encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)  # Ignorer l'en-tête
                    for row in reader:
                        try:
                            # Ajouter chaque ligne à la base de données
                            connection = create_connection()
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
                                    (row[0], row[1], row[2], row[3])
                                )
                            connection.commit()
                        except Exception as e:
                            print(f"Erreur lors de l'ajout du travail {row} : {str(e)}")
                        finally:
                            connection.close()
                messagebox.showinfo("Succès", "Travaux importés avec succès.")
                self.afficher_travaux()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'importation : {str(e)}")
