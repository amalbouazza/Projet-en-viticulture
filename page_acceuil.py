from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from database import create_connection  # Assurez-vous que cette fonction existe

class PageAcceuil(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Titre de la page d'accueil
        Label(self, text="Page d'Accueil - Analyses", font=("Arial", 24)).pack(pady=20)
        
        # Récupérer les données de la base de données
        self.donnees_x, self.donnees_y = self.get_data_from_db()
        
        # Afficher le graphique
        self.afficher_graphique()

    def get_data_from_db(self):
        """Récupérer les données réelles de la base de données"""
        connection = create_connection()
        
        # Requête pour obtenir la durée des travaux par ouvrier
        query = """
            SELECT o.nom, SUM(t.duree) AS duree_totale
            FROM travaux t
            JOIN ouvriers o ON t.ouvrier_id = o.id
            GROUP BY o.nom
            ORDER BY duree_totale DESC
        """
        # Lire les données dans un DataFrame
        df = pd.read_sql(query, connection)
        connection.close()

        # Extraire les données pour le graphique
        donnees_x = df['nom']  # Noms des ouvriers
        donnees_y = df['duree_totale']  # Durée totale des travaux pour chaque ouvrier
        
        return donnees_x, donnees_y

    def afficher_graphique(self):
        """Afficher un graphique sur la page d'accueil"""
        # Créer la figure pour le graphique avec des dimensions plus grandes
        figure = plt.Figure(figsize=(8, 5), dpi=70)  # Taille augmentée de (6, 4) à (10, 6)
        ax = figure.add_subplot(111)

        # Tracer les données sur le graphique
        ax.bar(self.donnees_x, self.donnees_y, color='skyblue')
        ax.set_title("Durée Totale des Travaux par Ouvrier", fontsize=16)
        ax.set_xlabel("Ouvrier", fontsize=14)
        ax.set_ylabel("Durée Totale des Travaux (heures)", fontsize=14)
        ax.tick_params(axis='x', rotation=45)  # Rotation des noms des ouvriers pour les rendre lisibles

        # Convertir la figure en un canvas Tkinter
        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(fill=BOTH, expand=1, pady=20)  # Faire en sorte que le canvas occupe plus d'espace
        canvas.draw()


