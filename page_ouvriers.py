from tkinter import *
from tkinter import messagebox, filedialog
import csv
from database import create_connection  # Assurez-vous que cette fonction existe et fonctionne correctement

class PageOuvriers(Frame):
    def __init__(self, parent, actualiser_callback):
        super().__init__(parent)
        self.parent = parent
        self.actualiser_callback = actualiser_callback  # Callback pour actualiser la liste des ouvriers dans PageTravaux

        Label(self, text="Gestion des Ouvriers", font=("Arial", 24)).pack(pady=20)

        # Formulaire pour l'ajout d'ouvriers manuellement
        Label(self, text="Nom :").pack()
        self.nom_entry = Entry(self)
        self.nom_entry.pack()

        Label(self, text="Prénom :").pack()
        self.prenom_entry = Entry(self)
        self.prenom_entry.pack()

        Button(self, text="Ajouter Ouvrier", command=self.ajouter_ouvrier).pack(pady=20)

        # Bouton pour ajouter des ouvriers via fichier
        Button(self, text="Ajouter Ouvriers via Fichier", command=self.ajouter_ouvriers_fichier).pack(pady=20)

    def ajouter_ouvrier(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()

        if nom and prenom:
            try:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))
                connection.commit()  # Valider la transaction
                messagebox.showinfo("Succès", f"Ouvrier {nom} {prenom} ajouté avec succès")

                # Appel du callback pour actualiser la liste dans la page des Travaux
                self.actualiser_callback()

                # Réinitialiser les champs
                self.nom_entry.delete(0, END)
                self.prenom_entry.delete(0, END)

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'ouvrier : {str(e)}")
            finally:
                connection.close()  # Fermer la connexion
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")

    def ajouter_ouvriers_fichier(self):
        # Ouvrir un dialogue pour sélectionner le fichier CSV
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        
        if not fichier:
            return  # Si aucun fichier n'est sélectionné, ne rien faire

        try:
            # Lire le fichier CSV avec le bon séparateur (';')
            with open(fichier, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')  # Utilisation du séparateur point-virgule
                next(reader)  # Si le fichier contient une ligne d'entête, la sauter
                
                # Connexion à la base de données
                connection = create_connection()
                if connection is None:
                    raise Exception("Échec de la connexion à la base de données.")
                
                with connection.cursor() as cursor:
                    for row in reader:
                        if len(row) == 2:  # Vérifier que chaque ligne contient bien 2 colonnes (nom, prénom)
                            nom, prenom = row
                            cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))

                    connection.commit()  # Valider toutes les insertions

            messagebox.showinfo("Succès", "Les ouvriers ont été ajoutés avec succès depuis le fichier.")
            
            # Appel du callback pour actualiser la liste des ouvriers dans la page Travaux
            self.actualiser_callback()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout des ouvriers depuis le fichier : {str(e)}")
        finally:
            if connection:
                connection.close()  # Fermer la connexion à la base de données
