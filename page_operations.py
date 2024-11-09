from tkinter import *
from tkinter import messagebox, ttk
from database import create_connection  # Assurer l'importation de la fonction de connexion

class PageOperations(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f4f4f4")  # Fond gris clair pour la page
        Label(self, text="Gestion des Opérations Phytosanitaires", font=("Arial", 24), bg="#f4f4f4").pack(pady=20)

        # Liste des maladies pour la combobox
        self.maladies = ["Mildiou", "Oïdium", "Botrytis", "Fusariose", "Verticilliose", "Autre"]

        # Liste des stades de la maladie pour la combobox
        self.stades = ["Début de développement", "Phase de propagation", "Phase de maturité", "Phase terminale"]

        # Liste des méthodes de traitement pour la combobox
        self.methodes = ["Traitement chimique", "Traitement biologique", "Mécanique", "Autre"]

        # Formulaire pour l'ajout d'opérations phytosanitaires
        self._create_label("Nom de la Maladie :")
        self.maladie_combobox = self._create_combobox(self.maladies)

        self._create_label("Stade de la Maladie :")
        self.stade_combobox = self._create_combobox(self.stades)

        self._create_label("Méthode de Traitement :")
        self.methode_combobox = self._create_combobox(self.methodes)

        self._create_label("Observations :")
        self.observations_entry = Text(self, height=5, width=40, wrap=WORD, bg="white", font=("Arial", 12))
        self.observations_entry.pack(pady=10)

        self._create_label("Sélectionner un Ouvrier :")
        self.ouvrier_combobox = ttk.Combobox(self, state="readonly")
        self.ouvrier_combobox.pack(pady=10)

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        # Bouton pour ajouter une opération phytosanitaire
        Button(self, text="Ajouter Opération", command=self.ajouter_operation, bg="#4CAF50", fg="white", font=("Arial", 12), relief=RAISED).pack(pady=20)

    def _create_label(self, text):
        """Créer un label stylisé."""
        Label(self, text=text, font=("Arial", 12), bg="#f4f4f4").pack(pady=5)

    def _create_combobox(self, values):
        """Créer une combobox avec un fond blanc et une bordure."""
        combobox = ttk.Combobox(self, values=values, font=("Arial", 12), state="readonly")
        combobox.pack(pady=5)
        return combobox

    def remplir_liste_ouvriers(self):
        """Remplir la liste déroulante avec les ouvriers de la base de données."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, nom FROM ouvriers")  # Assurez-vous que la table et les colonnes existent
                ouvriers = cursor.fetchall()
                # Ajouter les noms des ouvriers et leur ID dans la combobox
                self.ouvrier_combobox['values'] = [f"{ouvrier[0]} - {ouvrier[1]}" for ouvrier in ouvriers]
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des ouvriers : {str(e)}")
        finally:
            connection.close()

    def ajouter_operation(self):
        maladie = self.maladie_combobox.get()
        stade = self.stade_combobox.get()
        methode = self.methode_combobox.get()
        observations = self.observations_entry.get("1.0", END).strip()  # Obtenir le texte du widget Text
        
        # Récupérer l'ID de l'ouvrier à partir de la sélection dans la combobox
        selection = self.ouvrier_combobox.get()
        if selection:
            ouvrier_id = selection.split(' - ')[0]  # Récupérer uniquement l'ID
        else:
            ouvrier_id = None

        if maladie and stade and methode and ouvrier_id:
            try:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO phytosanitaire (maladie, stade, methode, observation, ouvrier_id) VALUES (%s, %s, %s, %s, %s)",
                        (maladie, stade, methode, observations, ouvrier_id)
                    )
                connection.commit()
                messagebox.showinfo("Succès", f"Opération pour '{maladie}' ajoutée avec succès")
                # Réinitialiser les champs
                self.maladie_combobox.set('')
                self.stade_combobox.set('')
                self.methode_combobox.set('')
                self.observations_entry.delete("1.0", END)  # Réinitialiser le champ de texte
                self.ouvrier_combobox.set('')  # Réinitialiser la sélection
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'opération : {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs requis")
