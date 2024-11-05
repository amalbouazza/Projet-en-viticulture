from tkinter import *
from tkinter import messagebox, ttk
from database import create_connection  # Importer la fonction de connexion

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

        Button(self, text="Ajouter Travail", command=self.ajouter_travail).pack(pady=20)

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
        
        # Récupérer l'ID de l'ouvrier à partir de la sélection dans la combobox
        selection = self.ouvrier_combobox.get()
        if selection:
            ouvrier_id = selection.split(' - ')[0]  # Récupérer uniquement l'ID
        else:
            ouvrier_id = None

        if type_travail and duree and ouvrier_id:
            try:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO travaux (type_travail, duree, ouvrier_id) VALUES (%s, %s, %s)",
                        (type_travail, duree, ouvrier_id)
                    )
                connection.commit()
                messagebox.showinfo("Succès", f"Travail '{type_travail}' ajouté avec succès")
                self.type_entry.delete(0, END)
                self.duree_entry.delete(0, END)
                self.ouvrier_combobox.set('')  # Réinitialiser la sélection
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout du travail : {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
