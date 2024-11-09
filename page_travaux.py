from tkinter import Frame, Label, Entry, Button, messagebox  # Ajout de Frame et autres widgets nécessaires
from tkinter import ttk, filedialog
from tkcalendar import Calendar
import csv
from database import create_connection  # Assurez-vous que cette fonction existe et fonctionne correctement

class PageTravaux(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()  # Assurez-vous que le frame est ajouté à l'interface
        Label(self, text="Gestion des Travaux", font=("Arial", 24)).pack(pady=20)

        # Formulaire pour l'ajout de travaux
        Label(self, text="Type de Travail :").pack()
        
        # Liste déroulante pour sélectionner le type de travail
        self.type_combobox = ttk.Combobox(self, values=[
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
        ])
        self.type_combobox.pack()
        self.type_combobox.bind("<<ComboboxSelected>>", self.on_type_selected)  # Lier l'événement de sélection à une fonction

        # Zone de texte pour "Autre" type de travail
        self.other_type_label = Label(self, text="Type de travail (si 'Autre') :")
        self.other_type_label.pack()
        self.other_type_entry = Entry(self)
        self.other_type_entry.pack()
        self.other_type_entry.pack_forget()  # Cacher la zone de texte par défaut

        Label(self, text="Durée (heures) :").pack()
        self.duree_entry = Entry(self)
        self.duree_entry.pack()

        Label(self, text="ID de l'Ouvrier :").pack()
        self.ouvrier_combobox = ttk.Combobox(self)
        self.ouvrier_combobox.pack()

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        # Zone de sélection de la date via le calendrier
        Label(self, text="Date du travail :").pack()
        self.calendrier = Calendar(self, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendrier.pack(pady=10)

        Button(self, text="Ajouter Travail", command=self.ajouter_travail).pack(pady=10)

        Button(self, text="Importer Travaux depuis Fichier", command=self.importer_travaux).pack(pady=10)

    def on_type_selected(self, event):
        """Fonction qui gère la sélection de type de travail."""
        selected_type = self.type_combobox.get()
        
       

    def remplir_liste_ouvriers(self):
        """Remplir la liste déroulante avec les IDs des ouvriers de la base de données."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom FROM ouvriers")  # Assure-toi que la table et les colonnes existent
                ouvriers = cursor.fetchall()
                # Ajouter les noms des ouvriers et leur ID dans la combobox
                self.ouvrier_combobox['values'] = [f"{ouvrier[0]} - {ouvrier[1]}" for ouvrier in ouvriers]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des ouvriers : {str(e)}")
        finally:
            connection.close()

    def ajouter_travail(self):
        type_travail = self.type_combobox.get()  # Récupérer la valeur sélectionnée dans le Combobox
        
        # Si le type de travail est "Autre", récupérer la valeur saisie dans la zone de texte
        if type_travail == "Autre":
            type_travail = self.other_type_entry.get()

        duree = self.duree_entry.get()
        date_travail = self.calendrier.get_date()  # Obtenir la date sélectionnée dans le calendrier
        
        # Récupérer l'ID de l'ouvrier à partir de la sélection dans la combobox
        selection = self.ouvrier_combobox.get()
        if selection:
            ouvrier_id = selection.split(' - ')[0]  # Récupérer uniquement l'ID
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

                # Message de succès
                messagebox.showinfo("Succès", f"Travail '{type_travail}' ajouté avec succès")

                # Réinitialiser les champs
                self.type_combobox.set('')  # Réinitialiser la sélection
                self.duree_entry.delete(0, 'end')
                self.ouvrier_combobox.set('')  # Réinitialiser la sélection
                self.calendrier.set_date('')  # Réinitialiser la date sélectionnée
                self.other_type_entry.delete(0, 'end')  # Réinitialiser la zone de texte

                # Masquer la zone de texte si un autre type est sélectionné
                self.other_type_entry.pack_forget()
                # Actualiser la liste des ouvriers dans la combobox après ajout du travail
                self.remplir_liste_ouvriers()

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du travail : {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")

    def importer_travaux(self):
        """Importer les travaux depuis un fichier CSV."""
        fichier = filedialog.askopenfilename(title="Sélectionner un fichier CSV", filetypes=[("CSV Files", "*.csv")])
        if fichier:
            try:
                with open(fichier, newline='', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)  # Sauter l'en-tête du CSV
                    for row in reader:
                        if len(row) == 4:  # Vérifier que chaque ligne contient les 4 champs attendus
                            type_travail, duree, ouvrier_id, date_travail = row
                            try:
                                # Vérifier que la durée est un nombre et la date est au bon format
                                duree = int(duree)  # S'assurer que la durée est un entier
                                # Insérer dans la base de données
                                connection = create_connection()
                                with connection.cursor() as cursor:
                                    cursor.execute(
                                        "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
                                        (type_travail, duree, ouvrier_id, date_travail)
                                    )
                                connection.commit()
                            except Exception as e:
                                messagebox.showerror("Erreur", f"Erreur lors de l'insertion du travail : {str(e)}")
                            finally:
                                connection.close()

                    messagebox.showinfo("Succès", "Travaux importés avec succès depuis le fichier CSV")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'importation des travaux : {str(e)}")
