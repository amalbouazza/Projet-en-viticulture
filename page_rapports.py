from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import scrolledtext
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from database import create_connection  # Assurez-vous que cette fonction existe

class PageRapport(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(padx=20, pady=20)

        # Titre de la page, style uniformisé
        self.title_label = Label(self, text="Gestion des Travaux Viticoles", font=("Arial", 24, 'bold'), bg="#f0f0f0", anchor="center")
        self.title_label.pack(pady=20, padx=10, fill='x')  # Centrer le titre

        # Création d'un cadre pour les boutons avec une belle disposition
        self.bouton_frame = Frame(self)
        self.bouton_frame.pack(pady=20, fill='x')

        self.bouton_rapport = Button(self.bouton_frame, text="Rapport Phytosanitaire", width=20, height=2, font=("Arial", 12), command=self.afficher_rapport)
        self.bouton_rapport.grid(row=0, column=0, padx=10)

        self.bouton_pdf = Button(self.bouton_frame, text="Exporter en PDF", width=20, height=2, font=("Arial", 12), command=self.exporter_pdf)
        self.bouton_pdf.grid(row=0, column=1, padx=10)

        self.bouton_stat = Button(self.bouton_frame, text="Analyse Statistique", width=20, height=2, font=("Arial", 12), command=self.analyser_statistique)
        self.bouton_stat.grid(row=0, column=2, padx=10)

        # Zone pour afficher les formulaires selon l'option choisie
        self.zone_formulaire = Frame(self)
        self.zone_formulaire.pack(pady=20, fill='x')

    def afficher_rapport(self):
        """Afficher le formulaire pour générer un rapport phytosanitaire"""
        self._clear_zone_formulaire()

        Label(self.zone_formulaire, text="Rapport des Opérations Phytosanitaires", font=("Arial", 18, 'bold')).pack(pady=10)

        self.rapport_text = scrolledtext.ScrolledText(self.zone_formulaire, height=25, width=100, wrap=WORD, font=("Arial", 10))
        self.rapport_text.pack(pady=10)

        Button(self.zone_formulaire, text="Générer Rapport", width=20, height=2, font=("Arial", 12), command=self.generer_rapport).pack(pady=10)

    def generer_rapport(self):
        """Générer le rapport des opérations phytosanitaires"""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("""SELECT p.maladie, p.stade, p.methode, p.observation, o.nom 
                                  FROM phytosanitaire p
                                  JOIN ouvriers o ON p.ouvrier_id = o.id
                                  ORDER BY p.maladie, p.stade""")
                operations = cursor.fetchall()

                if not operations:
                    messagebox.showinfo("Aucune Donnée", "Aucune opération phytosanitaire enregistrée.")
                    return

                self.rapport_text.config(state=NORMAL)
                self.rapport_text.delete(1.0, END)

                # Formatage du texte
                self.rapport_text.insert(END, "Maladie | Stade | Méthode | Observation | Ouvrier\n")
                self.rapport_text.insert(END, "-"*80 + "\n")

                for operation in operations:
                    self.rapport_text.insert(END, f"{operation[0]:<20} | {operation[1]:<10} | {operation[2]:<15} | {operation[3]:<20} | {operation[4]:<15}\n")

                self.rapport_text.config(state=DISABLED)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du rapport : {str(e)}")
        finally:
            if connection:
                connection.close()

    def exporter_pdf(self):
        """Exporter les données en PDF sous forme de tableau avec gestion de la mise en page"""
        try:
            fichier = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])
            if fichier:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute("""SELECT p.maladie, p.stade, p.methode, p.observation, o.nom 
                                      FROM phytosanitaire p
                                      JOIN ouvriers o ON p.ouvrier_id = o.id
                                      ORDER BY p.maladie, p.stade""")
                    operations = cursor.fetchall()

                if not operations:
                    messagebox.showinfo("Aucune Donnée", "Aucune opération phytosanitaire à exporter.")
                    return

                c = canvas.Canvas(fichier, pagesize=letter)
                c.setFont("Helvetica", 8)

                # Titre du rapport
                c.drawString(100, 750, "Rapport des Opérations Phytosanitaires")
                c.drawString(100, 735, "-----------------------------------------")

                # En-tête du tableau
                c.setFont("Helvetica-Bold", 10)
                c.drawString(100, 715, "Maladie")
                c.drawString(200, 715, "Stade")
                c.drawString(300, 715, "Méthode")
                c.drawString(400, 715, "Observation")
                c.drawString(500, 715, "Ouvrier")
                c.setFont("Helvetica", 8)

                # Ajouter les lignes du tableau avec espacement amélioré
                y_position = 700
                line_height = 15  # Espacement entre les lignes du tableau

                for operation in operations:
                    text = f"{operation[0]:<20} | {operation[1]:<10} | {operation[2]:<15} | {operation[3]:<20} | {operation[4]:<15}"
                    c.drawString(100, y_position, text)
                    y_position -= line_height

                    if y_position < 100:
                        c.showPage()  # Crée une nouvelle page
                        c.setFont("Helvetica", 8)
                        c.drawString(100, 750, "Rapport des Opérations Phytosanitaires")
                        c.drawString(100, 735, "-----------------------------------------")
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(100, 715, "Maladie")
                        c.drawString(200, 715, "Stade")
                        c.drawString(300, 715, "Méthode")
                        c.drawString(400, 715, "Observation")
                        c.drawString(500, 715, "Ouvrier")
                        y_position = 700  # Recommence à une position haute

                c.save()
                messagebox.showinfo("Succès", "Le rapport PDF a été généré avec succès.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {str(e)}")

    def analyser_statistique(self):
        """Analyser les durées des travaux avec régression linéaire"""
        self._clear_zone_formulaire()

        Label(self.zone_formulaire, text="Analyse Statistique des Travaux", font=("Arial", 18, 'bold')).pack(pady=10)

        Button(self.zone_formulaire, text="Analyser Durée des Travaux", width=20, height=2, font=("Arial", 12), command=self.analyser_duree).pack(pady=10)

    def analyser_duree(self):
        """Analyser les durées des travaux avec Machine Learning (Régression linéaire)"""
        try:
            connection = create_connection()
            query = """
                SELECT t.duree, o.nom, t.type_travail
                FROM travaux t
                JOIN ouvriers o ON t.ouvrier_id = o.id
            """
            df = pd.read_sql(query, connection)
            connection.close()

            # Utilisation de l'encodage One-Hot pour les variables catégorielles
            df = pd.get_dummies(df, columns=['nom', 'type_travail'], drop_first=True)

            X = df.drop('duree', axis=1)  # Variables explicatives
            y = df['duree']  # Variable cible (durée des travaux)

            # Création du modèle de régression linéaire
            model = LinearRegression()
            model.fit(X, y)

            messagebox.showinfo("Analyse", f"Coefficients : {model.coef_}\nIntercept : {model.intercept_}")

            # Visualisation des données réelles et de la prédiction du modèle
            plt.scatter(range(len(y)), y, color='blue', label='Données réelles')
            plt.plot(range(len(y)), model.predict(X), color='red', label='Régression linéaire')

            plt.title("Analyse de la Durée des Travaux")
            plt.xlabel('Index des Travaux')
            plt.ylabel('Durée (heures)')
            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse des données : {str(e)}")

    def _clear_zone_formulaire(self):
        """Effacer tous les widgets dans la zone formulaire"""
        for widget in self.zone_formulaire.winfo_children():
            widget.destroy()  # Effacer l'ancienne interface si existante
