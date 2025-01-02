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

        # Titre de la page, style standardisé
        self.title_label = Label(self, text="Gestion des Travaux Viticoles", font=("Arial", 24, 'bold'), bg="#f0f0f0", anchor="center")
        self.title_label.pack(pady=20, padx=10, fill='x')  # Titre centré

        # Frame pour les boutons avec une meilleure disposition
        self.bouton_frame = Frame(self)
        self.bouton_frame.pack(pady=20, fill='x')

        self.bouton_rapport = Button(self.bouton_frame, text="Rapport Phytosanitaire", width=20, height=2, font=("Arial", 12), command=self.afficher_rapport)
        self.bouton_rapport.grid(row=0, column=0, padx=10)

        self.bouton_pdf = Button(self.bouton_frame, text="Exporter en PDF", width=20, height=2, font=("Arial", 12), command=self.exporter_pdf)
        self.bouton_pdf.grid(row=0, column=1, padx=10)

        self.bouton_stat = Button(self.bouton_frame, text="Analyse Statistique", width=20, height=2, font=("Arial", 12), command=self.analyser_statistique)
        self.bouton_stat.grid(row=0, column=2, padx=10)

        # Frame pour afficher des formulaires selon le choix de l'utilisateur
        self.zone_formulaire = Frame(self)
        self.zone_formulaire.pack(pady=20, fill='x')

    def _clear_zone_formulaire(self):
        """Efface le contenu de la zone de formulaire avant d'afficher une nouvelle section"""
        for widget in self.zone_formulaire.winfo_children():
            widget.destroy()

    def afficher_rapport(self):
        """Affiche le formulaire pour générer un rapport phytosanitaire"""
        self._clear_zone_formulaire()

        Label(self.zone_formulaire, text="Rapport des Opérations Phytosanitaires", font=("Arial", 18, 'bold')).pack(pady=10)

        self.rapport_text = scrolledtext.ScrolledText(self.zone_formulaire, height=25, width=100, wrap=WORD, font=("Arial", 10))
        self.rapport_text.pack(pady=10)

        Button(self.zone_formulaire, text="Générer Rapport", width=20, height=2, font=("Arial", 12), command=self.generer_rapport).pack(pady=10)

    def generer_rapport(self):
        """Génère le rapport des opérations phytosanitaires"""
        connection = None
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

                # Format du texte pour affichage
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
        """Exporter les données au format PDF avec une disposition automatique du texte"""
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

                # En-têtes de tableau
                c.setFont("Helvetica-Bold", 10)
                c.drawString(100, 715, "Maladie")
                c.drawString(200, 715, "Stade")
                c.drawString(300, 715, "Méthode")
                c.drawString(400, 715, "Observation")
                c.drawString(500, 715, "Ouvrier")

                c.setFont("Helvetica", 8)

                # Ajouter les lignes du tableau sans gestion manuelle de position
                data = ["Maladie | Stade | Méthode | Observation | Ouvrier"]
                data.append("-" * 80)
                for operation in operations:
                    line = f"{operation[0]:<20} | {operation[1]:<10} | {operation[2]:<15} | {operation[3]:<20} | {operation[4]:<15}"
                    data.append(line)

                # Insérer les lignes dans le PDF
                y_position = 1000
                line_height = 15  # Hauteur de ligne entre les lignes
                for line in data:
                    c.drawString(100, y_position, line)
                    y_position -= line_height

                    # Nouvelle page si l'espace est insuffisant
                    if y_position < 100:
                        c.showPage()
                        c.setFont("Helvetica", 8)
                        c.drawString(100, 750, "Rapport des Opérations Phytosanitaires")
                        c.drawString(100, 735, "-----------------------------------------")
                        c.setFont("Helvetica-Bold", 10)
                        c.drawString(100, 715, "Maladie")
                        c.drawString(200, 715, "Stade")
                        c.drawString(300, 715, "Méthode")
                        c.drawString(400, 715, "Observation")
                        c.drawString(500, 715, "Ouvrier")
                        y_position = 680  # Repartir en haut pour la page suivante

                c.save()
                messagebox.showinfo("Succès", "Le rapport PDF a été généré avec succès.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la génération du PDF : {str(e)}")

    def analyser_statistique(self):
        """Analyser les durées des travaux avec une régression linéaire"""
        self._clear_zone_formulaire()

        Label(self.zone_formulaire, text="Analyse Statistique des Travaux", font=("Arial", 18, 'bold')).pack(pady=10)

        Button(self.zone_formulaire, text="Analyser Durée des Travaux", width=20, height=2, font=("Arial", 12), command=self.analyser_duree).pack(pady=10)

    def analyser_duree(self):
        """Analyser les durées des travaux avec apprentissage automatique (Régression linéaire)"""
        try:
            connection = create_connection()
            query = """
                SELECT t.duree, o.nom, t.type_travail
                FROM travaux t
                JOIN ouvriers o ON t.ouvrier_id = o.id
            """
            df = pd.read_sql(query, connection)
            connection.close()

            if df.empty:
                messagebox.showinfo("Aucune donnée", "Aucune donnée trouvée pour l'analyse.")
                return

            df = pd.get_dummies(df, columns=['nom', 'type_travail'], drop_first=True)
            X = df.drop('duree', axis=1)
            y = df['duree']

            model = LinearRegression()
            model.fit(X, y)

            messagebox.showinfo("Analyse", f"Coefficients : {model.coef_}\nIntercept : {model.intercept_}")

            plt.figure(figsize=(10, 6))
            y_pred = model.predict(X)
            plt.scatter(y, y_pred, color='blue', label='Durées prédites', alpha=0.7)
            plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red', lw=2, label='Ligne de Régression')
            plt.xlabel('Durée réelle')
            plt.ylabel('Durée prédite')
            plt.title('Analyse de la durée des travaux (Régression linéaire)')
            plt.legend()
            plt.grid(True)
            plt.show()

        except Exception as e:
            messagebox.showerror("Erreur d'Analyse", f"Erreur lors de l'analyse des durées : {str(e)}")
