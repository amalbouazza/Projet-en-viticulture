from tkinter import *
from tkinter import messagebox, ttk, filedialog
from tkcalendar import Calendar
import csv
from database import create_connection  # Assurez-vous que cette fonction existe et fonctionne correctement

class PageTravaux(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Gestion des Travaux", font=("Arial", 24)).pack(pady=20)

        # Formulaire pour l'ajout de travaux
        Label(self, text="Type de Travail :").pack()
        self.type_entry = Entry(self)
        self.type_entry.pack()

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
        type_travail = self.type_entry.get()
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
                self.type_entry.delete(0, END)
                self.duree_entry.delete(0, END)
                self.ouvrier_combobox.set('')  # Réinitialiser la sélection
                self.calendrier.set_date('')  # Réinitialiser la date sélectionnée

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
                            # Insérer dans la base de données
                            connection = create_connection()
                            with connection.cursor() as cursor:
                                cursor.execute(
                                    "INSERT INTO travaux (type_travail, duree, ouvrier_id, date_travail) VALUES (%s, %s, %s, %s)",
                                    (type_travail, duree, ouvrier_id, date_travail)
                                )
                            connection.commit()
                            connection.close()

                    messagebox.showinfo("Succès", "Travaux importés avec succès depuis le fichier CSV")
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'importation des travaux : {str(e)}")
