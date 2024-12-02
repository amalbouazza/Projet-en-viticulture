from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv
from database import create_connection  # Assurez-vous que cette fonction existe et fonctionne correctement


class PageOuvriers(Frame):
    def __init__(self, parent, actualiser_callback):
        super().__init__(parent)
        self.parent = parent
        self.actualiser_callback = actualiser_callback  # Callback pour actualiser d'autres pages si nécessaire

        # Personnalisation de l'interface avec des couleurs de fond et des polices
        self.configure(bg="#f4f4f4")

        # Titre
        title_label = Label(self, text="Gestion des Ouvriers", font=("Arial", 24, "bold"), bg="#f4f4f4", fg="#333333")
        title_label.pack(pady=20)

        # Formulaire pour l'ajout d'ouvriers manuellement
        Label(self, text="Nom :", font=("Arial", 14), bg="#f4f4f4").pack()
        self.nom_entry = Entry(self, font=("Arial", 12), width=30, relief="solid", bd=1, bg="#ffffff")
        self.nom_entry.pack(pady=5)

        Label(self, text="Prénom :", font=("Arial", 14), bg="#f4f4f4").pack()
        self.prenom_entry = Entry(self, font=("Arial", 12), width=30, relief="solid", bd=1, bg="#ffffff")
        self.prenom_entry.pack(pady=5)

        # Boutons personnalisés
        bouton_ajouter = Button(self, text="Ajouter Ouvrier", command=self.ajouter_ouvrier, font=("Arial", 12),
                                bg="#4CAF50", fg="white", relief="raised", bd=2)
        bouton_ajouter.pack(pady=10)

        bouton_fichier = Button(self, text="Ajouter Ouvriers via Fichier", command=self.ajouter_ouvriers_fichier,
                                font=("Arial", 12), bg="#008CBA", fg="white", relief="raised", bd=2)
        bouton_fichier.pack(pady=10)

        # Tableau pour afficher la liste des ouvriers
        self.tree = ttk.Treeview(self, columns=("ID", "Nom", "Prénom"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nom", text="Nom")
        self.tree.heading("Prénom", text="Prénom")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Nom", width=150, anchor="center")
        self.tree.column("Prénom", width=150, anchor="center")

        self.tree.pack(pady=20, fill=BOTH, expand=True)

        # Charger la liste des ouvriers au démarrage
        self.charger_ouvriers()

    def charger_ouvriers(self):
        """Charger et afficher la liste des ouvriers depuis la base de données."""
        # Effacer le contenu existant du Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom, prenom FROM ouvriers")
                rows = cursor.fetchall()
                # Ajouter chaque ligne dans le Treeview
                for row in rows:
                    self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des ouvriers : {str(e)}")
        finally:
            if connection:
                connection.close()

    def ajouter_ouvrier(self):
        """Ajouter un ouvrier manuellement dans la base de données."""
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()

        if nom and prenom:
            try:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))
                connection.commit()  # Valider la transaction
                messagebox.showinfo("Succès", f"Ouvrier {nom} {prenom} ajouté avec succès")

                # Actualiser la liste des ouvriers
                self.charger_ouvriers()

                # Réinitialiser les champs
                self.nom_entry.delete(0, END)
                self.prenom_entry.delete(0, END)

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'ouvrier : {str(e)}")
            finally:
                if connection:
                    connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs")

    def ajouter_ouvriers_fichier(self):
        """Ajouter des ouvriers depuis un fichier CSV."""
        fichier = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])
        if not fichier:
            return  # Si aucun fichier n'est sélectionné, ne rien faire

        try:
            with open(fichier, mode='r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')  # Utilisation du séparateur point-virgule
                next(reader)  # Sauter l'entête

                connection = create_connection()
                with connection.cursor() as cursor:
                    for row in reader:
                        if len(row) == 2:
                            nom, prenom = row
                            cursor.execute("INSERT INTO ouvriers (nom, prenom) VALUES (%s, %s)", (nom, prenom))
                connection.commit()

            messagebox.showinfo("Succès", "Les ouvriers ont été ajoutés depuis le fichier.")
            self.charger_ouvriers()  # Actualiser la liste après ajout

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout des ouvriers depuis le fichier : {str(e)}")
        finally:
            if connection:
                connection.close()
