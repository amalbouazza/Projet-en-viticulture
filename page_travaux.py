from tkinter import Frame, Label, Entry, Button, messagebox
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import csv
import joblib  # Pour charger le modèle ML
from database import create_connection  # Assurez-vous que cette fonction existe et fonctionne correctement


class PageTravaux(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=10, pady=10)  # Ajout d'un espacement général autour du frame
        self.configure(bg="#f4f4f4")  # Fond de la page

        # Charger le modèle ML
        self.model = joblib.load("ml_models/ml_models/type_travail_model.pkl")  # Remplacez par le chemin réel de votre modèle

        # Titre
        title_label = Label(self, text="Gestion des Travaux", font=("Arial", 24, "bold"), bg="#f4f4f4", fg="#333333")
        title_label.pack(pady=20)

        # Frame pour organiser les champs
        form_frame = Frame(self, bg="#f4f4f4")
        form_frame.pack(pady=10)

        # Type de Travail et Durée
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

        # Ouvrier et Date du travail
        Label(form_frame, text="ID de l'Ouvrier :", font=("Arial", 14), bg="#f4f4f4").grid(row=2, column=0, pady=5)
        self.ouvrier_combobox = ttk.Combobox(form_frame, font=("Arial", 12))
        self.ouvrier_combobox.grid(row=2, column=1, pady=5)

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        Label(form_frame, text="Date du travail :", font=("Arial", 14), bg="#f4f4f4").grid(row=3, column=0, pady=5)
        self.calendrier = Calendar(form_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendrier.grid(row=3, column=1, pady=10)

        # Boutons
        bouton_frame = Frame(self, bg="#f4f4f4")
        bouton_frame.pack(pady=(10, 5))

        bouton_ajouter = Button(bouton_frame, text="Ajouter Travail", command=self.ajouter_travail, font=("Arial", 12),
                                bg="#4CAF50", fg="white", relief="raised", bd=2)
        bouton_ajouter.grid(row=0, column=0, padx=10)

        bouton_importer = Button(bouton_frame, text="Importer Travaux depuis Fichier", command=self.importer_travaux,
                                 font=("Arial", 12), bg="#008CBA", fg="white", relief="raised", bd=2)
        bouton_importer.grid(row=0, column=1, padx=10)

        # Table des travaux
        self.tree = ttk.Treeview(self, columns=("ID", "Type", "Durée", "Ouvrier", "Date"), show="headings", height=8)
        self.tree.pack(pady=(20, 10))

        # Définir les colonnes
        self.tree.heading("ID", text="ID")
        self.tree.heading("Type", text="Type de Travail")
        self.tree.heading("Durée", text="Durée (heures)")
        self.tree.heading("Ouvrier", text="Ouvrier")
        self.tree.heading("Date", text="Date du Travail")

        # Afficher les travaux existants
        self.afficher_travaux()

        # Section Prédiction
        Label(self, text="Prédire le Type de Travail", font=("Arial", 18, "bold"), bg="#f4f4f4", fg="#333333").pack(pady=(20, 10))

        predict_frame = Frame(self, bg="#f4f4f4")
        predict_frame.pack(pady=10)

        Label(predict_frame, text="ID de l'Ouvrier :", font=("Arial", 14), bg="#f4f4f4").grid(row=0, column=0, pady=5, padx=10)
        self.predict_ouvrier = ttk.Combobox(predict_frame, font=("Arial", 12))
        self.predict_ouvrier.grid(row=0, column=1, pady=5)

        Label(predict_frame, text="Durée (heures) :", font=("Arial", 14), bg="#f4f4f4").grid(row=1, column=0, pady=5, padx=10)
        self.predict_duree = Entry(predict_frame, font=("Arial", 12), relief="solid", bd=1, width=20)
        self.predict_duree.grid(row=1, column=1, pady=5)

        Label(predict_frame, text="Date (YYYY-MM-DD) :", font=("Arial", 14), bg="#f4f4f4").grid(row=2, column=0, pady=5, padx=10)
        self.predict_date = Entry(predict_frame, font=("Arial", 12), relief="solid", bd=1, width=20)
        self.predict_date.grid(row=2, column=1, pady=5)

        Button(predict_frame, text="Prédire", command=self.predire_travail, font=("Arial", 12), bg="#FF5722", fg="white",
               relief="raised", bd=2).grid(row=3, column=0, columnspan=2, pady=20)

    def remplir_liste_ouvriers(self):
        """Remplir la liste déroulante avec les ouvriers de la base de données."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom FROM ouvriers")
                ouvriers = cursor.fetchall()
                self.ouvrier_combobox['values'] = [f"{ouvrier[0]} - {ouvrier[1]}" for ouvrier in ouvriers]
                self.predict_ouvrier['values'] = [f"{ouvrier[0]} - {ouvrier[1]}" for ouvrier in ouvriers]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des ouvriers : {str(e)}")
        finally:
            connection.close()

    def ajouter_travail(self):
        """Ajouter un travail dans la base de données."""
        # Logique de l'ajout inchangée...
        pass

    def afficher_travaux(self):
        """Afficher tous les travaux dans le Treeview."""
        # Logique inchangée...
        pass

    def importer_travaux(self):
        """Importer les travaux depuis un fichier CSV."""
        # Logique inchangée...
        pass

    def predire_travail(self):
        """Prédire le type de travail."""
        try:
            selection = self.predict_ouvrier.get()
            ouvrier_id = selection.split(' - ')[0] if selection else None
            duree = self.predict_duree.get()
            date_travail = self.predict_date.get()

            if not (ouvrier_id and duree and date_travail):
                messagebox.showwarning("Erreur", "Veuillez remplir tous les champs pour effectuer une prédiction.")
                return

            # Formatage des données
            data = [[int(ouvrier_id), float(duree)]]

            # Prédiction
            prediction = self.model.predict(data)

            messagebox.showinfo("Résultat de la Prédiction", f"Type de travail prédit : {prediction[0]}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la prédiction : {str(e)}")
