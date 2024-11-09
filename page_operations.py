from tkinter import *
from tkinter import messagebox, ttk
from database import create_connection  # Assurer l'importation de la fonction de connexion

class PageOperations(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Gestion des Opérations Phytosanitaires", font=("Arial", 24)).pack(pady=20)

        # Liste des maladies pour la combobox
        self.maladies = ["Mildiou", "Oïdium", "Botrytis", "Fusariose", "Verticilliose", "Autre"]

        # Liste des stades de la maladie pour la combobox
        self.stades = ["Début de développement", "Phase de propagation", "Phase de maturité", "Phase terminale"]

        # Liste des méthodes de traitement pour la combobox
        self.methodes = ["Traitement chimique", "Traitement biologique", "Mécanique", "Autre"]

        # Formulaire pour l'ajout d'opérations phytosanitaires
        Label(self, text="Nom de la Maladie :").pack()
        self.maladie_combobox = ttk.Combobox(self, values=self.maladies)
        self.maladie_combobox.pack()

        Label(self, text="Stade de la Maladie :").pack()
        self.stade_combobox = ttk.Combobox(self, values=self.stades)
        self.stade_combobox.pack()

        Label(self, text="Méthode de Traitement :").pack()
        self.methode_combobox = ttk.Combobox(self, values=self.methodes)
        self.methode_combobox.pack()

        Label(self, text="Observations :").pack()
        self.observations_entry = Text(self, height=5, width=40)
        self.observations_entry.pack()

        Label(self, text="Sélectionner un Ouvrier :").pack()
        self.ouvrier_combobox = ttk.Combobox(self)
        self.ouvrier_combobox.pack()

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        Button(self, text="Ajouter Opération", command=self.ajouter_operation).pack(pady=20)

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
