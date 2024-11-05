from tkinter import *
from tkinter import messagebox
from database import create_connection  # Importer la fonction de connexion

class PageOuvriers(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Gestion des Ouvriers", font=("Arial", 24)).pack(pady=20)

        # Formulaire pour l'ajout d'ouvriers
        Label(self, text="Nom :").pack()
        self.nom_entry = Entry(self)
        self.nom_entry.pack()

        Label(self, text="Prénom :").pack()
        self.prenom_entry = Entry(self)
        self.prenom_entry.pack()

        Button(self, text="Ajouter Ouvrier", command=self.ajouter_ouvrier).pack(pady=20)

    def ajouter_ouvrier(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()

        if nom and prenom:
            try:
                connection = create_connection()  # Utiliser la fonction de connexion
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))
                connection.commit()  # Valider la transaction
                messagebox.showinfo("Succès", f"Ouvrier {nom} {prenom} ajouté avec succès")
                self.nom_entry.delete(0, END)  # Réinitialiser le champ
                self.prenom_entry.delete(0, END)  # Réinitialiser le champ
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'ouvrier : {str(e)}")
            finally:
                connection.close()  # Fermer la connexion
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")
