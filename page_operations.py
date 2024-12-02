from tkinter import *
from tkinter import messagebox, ttk
from database import create_connection  # Assurer l'importation de la fonction de connexion

class PageOperations(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f4f4f4")  # Fond gris clair pour la page
        Label(self, text="Gestion des Opérations Phytosanitaires", font=("Arial", 24), bg="#f4f4f4").pack(pady=20)

        # Conteneur principal pour la mise en page
        form_frame = Frame(self, bg="#f4f4f4")
        form_frame.pack(pady=10, padx=20, fill=X)

        # Ajouter des sous-conteneurs pour une disposition en colonnes
        left_frame = Frame(form_frame, bg="#f4f4f4")
        left_frame.pack(side=LEFT, padx=10, fill=X, expand=True)

        right_frame = Frame(form_frame, bg="#f4f4f4")
        right_frame.pack(side=RIGHT, padx=10, fill=X, expand=True)

        # Liste des maladies pour la combobox
        self.maladies = ["Mildiou", "Oïdium", "Botrytis", "Fusariose", "Verticilliose", "Autre"]

        # Liste des stades de la maladie pour la combobox
        self.stades = ["Début de développement", "Phase de propagation", "Phase de maturité", "Phase terminale"]

        # Liste des méthodes de traitement pour la combobox
        self.methodes = ["Traitement chimique", "Traitement biologique", "Mécanique", "Autre"]

        # Colonne gauche
        self._create_label(left_frame, "Nom de la Maladie :")
        self.maladie_combobox = self._create_combobox(left_frame, self.maladies)

        self._create_label(left_frame, "Stade de la Maladie :")
        self.stade_combobox = self._create_combobox(left_frame, self.stades)

        # Colonne droite
        self._create_label(right_frame, "Méthode de Traitement :")
        self.methode_combobox = self._create_combobox(right_frame, self.methodes)

        self._create_label(right_frame, "Sélectionner un Ouvrier :")
        self.ouvrier_combobox = ttk.Combobox(right_frame, state="readonly", font=("Arial", 12))
        self.ouvrier_combobox.pack(pady=5, fill=X)

        # Remplir la liste déroulante avec les ouvriers
        self.remplir_liste_ouvriers()

        # Observations sur toute la largeur
        self._create_label(self, "Observations :")
        self.observations_entry = Text(self, height=5, width=60, wrap=WORD, bg="white", font=("Arial", 12))
        self.observations_entry.pack(pady=10, padx=20)

        # Bouton pour ajouter une opération phytosanitaire
        Button(self, text="Ajouter Opération", command=self.ajouter_operation, bg="#4CAF50", fg="white", font=("Arial", 12), relief=RAISED).pack(pady=20)

        # Liste des opérations phytosanitaires
        self._create_label(self, "Liste des Opérations Phytosanitaires :")
        self.operations_tree = ttk.Treeview(self, columns=("Maladie", "Stade", "Méthode", "Observations", "Ouvrier"), show="headings", height=10)
        self.operations_tree.heading("Maladie", text="Maladie")
        self.operations_tree.heading("Stade", text="Stade")
        self.operations_tree.heading("Méthode", text="Méthode")
        self.operations_tree.heading("Observations", text="Observations")
        self.operations_tree.heading("Ouvrier", text="Ouvrier")
        self.operations_tree.pack(pady=10, padx=20, fill=BOTH, expand=True)

        # Ajouter une barre de défilement pour la liste
        scroll = ttk.Scrollbar(self, orient="vertical", command=self.operations_tree.yview)
        self.operations_tree.configure(yscroll=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)

        # Charger les opérations existantes dans la liste
        self.charger_operations()

    def _create_label(self, parent, text):
        """Créer un label stylisé."""
        Label(parent, text=text, font=("Arial", 12), bg="#f4f4f4").pack(pady=5, anchor="w")

    def _create_combobox(self, parent, values):
        """Créer une combobox avec un fond blanc et une bordure."""
        combobox = ttk.Combobox(parent, values=values, font=("Arial", 12), state="readonly")
        combobox.pack(pady=5, fill=X)
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
        observations = self.observations_entry.get("1.0", END).strip()

        selection = self.ouvrier_combobox.get()
        if selection:
            ouvrier_id = selection.split(' - ')[0]
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
                self.charger_operations()
                self.maladie_combobox.set('')
                self.stade_combobox.set('')
                self.methode_combobox.set('')
                self.observations_entry.delete("1.0", END)
                self.ouvrier_combobox.set('')
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'ajout de l'opération : {str(e)}")
            finally:
                connection.close()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs requis")

    def charger_operations(self):
        """Charger les opérations phytosanitaires dans la liste."""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("SELECT maladie, stade, methode, observation, ouvrier_id FROM phytosanitaire")
                operations = cursor.fetchall()
                for row in self.operations_tree.get_children():
                    self.operations_tree.delete(row)
                for operation in operations:
                    self.operations_tree.insert("", END, values=operation)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du chargement des opérations : {str(e)}")
        finally:
            connection.close()
