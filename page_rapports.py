import pandas as pd
from tkinter import scrolledtext
from tkinter import *
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class PageRapport(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=20, pady=20)

        # Titre de la page
        self.title_label = Label(self, text="Gestion des Travaux Viticoles", font=("Arial", 24, 'bold'), bg="#f0f0f0", anchor="center")
        self.title_label.pack(pady=20, padx=10, fill='x')

        # Cadre pour les boutons
        self.bouton_frame = Frame(self)
        self.bouton_frame.pack(pady=20, fill='x')


        self.bouton_pdf = Button(self.bouton_frame, text="Exporter en PDF", width=20, height=2, font=("Arial", 12), command=self.exporter_pdf)
        self.bouton_pdf.grid(row=0, column=1, padx=10)

        self.bouton_stat = Button(self.bouton_frame, text="Analyse Statistique", width=20, height=2, font=("Arial", 12), command=self.analyser_statistique)
        self.bouton_stat.grid(row=0, column=2, padx=10)

        # Nouveau bouton pour afficher le graphique
        self.bouton_graphique = Button(self.bouton_frame, text="Afficher Graphique", width=20, height=2, font=("Arial", 12), command=self.afficher_graphique)
        self.bouton_graphique.grid(row=1, column=0, padx=10, pady=10)

        # Zone pour afficher les formulaires selon l'option choisie
        self.zone_formulaire = Frame(self)
        self.zone_formulaire.pack(pady=20, fill='x')


    def generer_rapport(self):
        """Générer le rapport des opérations phytosanitaires"""
        # Code de génération du rapport
        pass

    def exporter_pdf(self):
        """Exporter les données en PDF sous forme de tableau avec gestion de la mise en page"""
        # Code pour exporter en PDF
        pass

    def analyser_statistique(self):
        """Analyser les durées des travaux avec régression linéaire"""
        # Code pour l'analyse statistique
        pass

    def afficher_graphique(self):
        """Afficher le graphique avec les données du fichier CSV après prédiction"""
        try:
            # Demander à l'utilisateur de sélectionner le fichier CSV
            file_path = filedialog.askopenfilename(title="Sélectionner le fichier CSV", filetypes=[("Fichiers CSV", "*.csv")])
            if not file_path:
                return

            # Charger les données du fichier CSV
            df = pd.read_csv(file_path)

            # Vérifier la présence des colonnes nécessaires
            if 'duree' not in df.columns or 'nom' not in df.columns or 'type_travail' not in df.columns:
                messagebox.showerror("Erreur", "Le fichier CSV ne contient pas les colonnes nécessaires.")
                return

            # Utilisation de l'encodage One-Hot pour les variables catégorielles
            df_encoded = pd.get_dummies(df, columns=['nom', 'type_travail'], drop_first=True)

            # Variables explicatives (X) et cible (y)
            X = df_encoded.drop('duree', axis=1)  # Variables explicatives
            y = df_encoded['duree']  # Variable cible (durée des travaux)

            # Créer et entraîner le modèle de régression linéaire
            model = LinearRegression()
            model.fit(X, y)

            # Prédictions avec le modèle
            predictions = model.predict(X)

            # Afficher les données réelles et les prédictions dans un graphique
            plt.figure(figsize=(10, 6))
            plt.scatter(range(len(y)), y, color='blue', label='Données réelles', alpha=0.5)
            plt.plot(range(len(y)), predictions, color='red', label='Prédictions (Régression linéaire)', linewidth=2)

            plt.title("Analyse des Durées des Travaux - Données et Prédictions")
            plt.xlabel('Index des Travaux')
            plt.ylabel('Durée (heures)')
            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage du graphique : {str(e)}")

    def _clear_zone_formulaire(self):
        """Effacer la zone de formulaire actuelle"""
        for widget in self.zone_formulaire.winfo_children():
            widget.destroy()
