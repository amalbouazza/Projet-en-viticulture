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
        self.pack(padx=10, pady=10)

        self.title_label = Label(self, text="Gestion des Travaux Viticoles", font=("Arial", 24))
        self.title_label.pack(pady=10)

        # Création d'un cadre pour les boutons
        self.bouton_frame = Frame(self)
        self.bouton_frame.pack(pady=10)

        self.bouton_rapport = Button(self.bouton_frame, text="Rapport Phytosanitaire", command=self.afficher_rapport)
        self.bouton_rapport.grid(row=0, column=0, padx=10)

        self.bouton_pdf = Button(self.bouton_frame, text="Exporter en PDF", command=self.exporter_pdf)
        self.bouton_pdf.grid(row=0, column=1, padx=10)

        self.bouton_stat = Button(self.bouton_frame, text="Analyse Statistique", command=self.analyser_statistique)
        self.bouton_stat.grid(row=0, column=2, padx=10)

        # Zone pour afficher les formulaires selon l'option choisie
        self.zone_formulaire = Frame(self)
        self.zone_formulaire.pack(pady=20)

    def afficher_rapport(self):
        """Afficher le formulaire pour générer un rapport phytosanitaire"""
        for widget in self.zone_formulaire.winfo_children():
            widget.destroy()  # Effacer l'ancienne interface si existante

        Label(self.zone_formulaire, text="Rapport des Opérations Phytosanitaires", font=("Arial", 18)).pack(pady=10)

        self.rapport_text = scrolledtext.ScrolledText(self.zone_formulaire, height=25, width=100)
        self.rapport_text.pack(pady=10)

        Button(self.zone_formulaire, text="Générer Rapport", command=self.generer_rapport).pack(pady=10)

    def generer_rapport(self):
        """Générer le rapport des opérations phytosanitaires"""
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT p.maladie, p.stade, p.methode, p.observation, o.nom 
                    FROM phytosanitaire p
                    JOIN ouvriers o ON p.ouvrier_id = o.id
                    ORDER BY p.maladie, p.stade
                """)
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
            connection.close()

    def exporter_pdf(self):
        """Exporter les données en PDF sous forme de tableau avec gestion de la mise en page"""
        try:
            fichier = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Fichiers PDF", "*.pdf")])
            if fichier:
                connection = create_connection()
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT p.maladie, p.stade, p.methode, p.observation, o.nom 
                        FROM phytosanitaire p
                        JOIN ouvriers o ON p.ouvrier_id = o.id
                        ORDER BY p.maladie, p.stade
                    """)
                    operations = cursor.fetchall()

                if not operations:
                    messagebox.showinfo("Aucune Donnée", "Aucune opération phytosanitaire à exporter.")
                    return

                c = canvas.Canvas(fichier, pagesize=letter)
                c.setFont("Helvetica", 8)

                # Titre du rapport
                c.drawString(100, 750, "Rapport des Opérations Phytosanitaires")
                c.drawString(100, 735, "-----------------------------------------")

                # En-tête du tableau avec une taille de police plus grande
                c.setFont("Helvetica-Bold", 10)
                c.drawString(100, 715, "Maladie")
                c.drawString(200, 715, "Stade")
                c.drawString(300, 715, "Méthode")
                c.drawString(400, 715, "Observation")
                c.drawString(500, 715, "Ouvrier")
                c.setFont("Helvetica", 8)

                # Variable pour la position verticale du texte (lignes du tableau)
                y_position = 700
                line_height = 12  # Espacement entre les lignes du tableau

                # Ajouter les lignes du tableau
                for operation in operations:
                    text = f"{operation[0]:<20} | {operation[1]:<10} | {operation[2]:<15} | {operation[3]:<20} | {operation[4]:<15}"
                    c.drawString(100, y_position, text)
                    y_position -= line_height

                    # Si on atteint le bas de la page, on passe à la nouvelle page
                    if y_position < 100:
                        c.showPage()  # Crée une nouvelle page
                        c.setFont("Helvetica", 8)
                        # En-tête sur la nouvelle page
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
        for widget in self.zone_formulaire.winfo_children():
            widget.destroy()  # Effacer l'ancienne interface si existante

        Label(self.zone_formulaire, text="Analyse Statistique des Travaux", font=("Arial", 18)).pack(pady=10)

        Button(self.zone_formulaire, text="Analyser Durée des Travaux", command=self.analyser_duree).pack(pady=10)

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

            df['ouvrier_id'] = pd.factorize(df['nom'])[0]
            df['type_travail_id'] = pd.factorize(df['type_travail'])[0]

            X = df[['ouvrier_id', 'type_travail_id']]
            y = df['duree']

            model = LinearRegression()
            model.fit(X, y)

            messagebox.showinfo("Analyse", f"Coefficients : {model.coef_}\nIntercept : {model.intercept_}")

            plt.scatter(df['ouvrier_id'], y, color='blue', label='Données réelles')
            plt.plot(df['ouvrier_id'], model.predict(X), color='red', label='Régression linéaire')
            plt.title("Analyse de la Durée des Travaux")
            plt.xlabel('ID Ouvrier')
            plt.ylabel
            plt.ylabel('Durée (heures)')
            plt.legend()
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'analyse des données : {str(e)}")
