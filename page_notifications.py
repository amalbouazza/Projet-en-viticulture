from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv("notif.env")

class PageNotifications(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#f4f4f4")  # Fond de la page
        
        # Titre de la page
        Label(self, text="Envoyer une Notification", font=("Arial", 24), bg="#f4f4f4").pack(pady=20)

        # Champ pour le destinataire
        self._create_label("Destinataire :")
        self.destinataire_entry = Entry(self, font=("Arial", 12), width=40)
        self.destinataire_entry.pack(pady=10)

        # Champ pour le sujet
        self._create_label("Sujet :")
        self.sujet_entry = Entry(self, font=("Arial", 12), width=40)
        self.sujet_entry.pack(pady=10)

        # Champ pour le message
        self._create_label("Message :")
        self.message_text = Text(self, height=10, width=40, font=("Arial", 12))
        self.message_text.pack(pady=10)

        # Bouton pour envoyer la notification
        Button(self, text="Envoyer Notification", command=self.envoyer_notification, bg="#4CAF50", fg="white", font=("Arial", 12), relief=RAISED).pack(pady=20)

    def _create_label(self, text):
        """Créer un label stylisé."""
        Label(self, text=text, font=("Arial", 12), bg="#f4f4f4").pack(pady=5)

    def envoyer_notification(self):
        """Fonction pour envoyer la notification par email."""
        destinataire = self.destinataire_entry.get()
        sujet = self.sujet_entry.get()
        message = self.message_text.get("1.0", END).strip()

        if destinataire and sujet and message:
            try:
                # Paramètres de connexion à Gmail (ou autre serveur SMTP)
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587

                # Utilisation des variables d'environnement pour la sécurité
                smtp_user = os.getenv('SMTP_USER')  # Email utilisateur (doit être dans le fichier .env)
                smtp_password = os.getenv('SMTP_PASSWORD')  # Mot de passe de l'application (doit être dans le fichier .env)

                if not smtp_user or not smtp_password:
                    raise ValueError("Le mot de passe ou l'adresse email n'est pas configuré dans les variables d'environnement.")

                # Création du message MIME
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = destinataire
                msg['Subject'] = sujet
                msg.attach(MIMEText(message, 'plain'))

                # Connexion et envoi de l'e-mail via le serveur SMTP
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Sécuriser la connexion
                    server.login(smtp_user, smtp_password)  # Se connecter au serveur
                    server.send_message(msg)  # Envoyer le message

                # Affichage d'un message de succès
                messagebox.showinfo("Succès", "Notification envoyée avec succès")

                # Réinitialiser les champs après envoi
                self.destinataire_entry.delete(0, END)
                self.sujet_entry.delete(0, END)
                self.message_text.delete("1.0", END)

            except smtplib.SMTPException as e:
                # Gestion des erreurs SMTP (problèmes de connexion, d'authentification, etc.)
                messagebox.showerror("Erreur SMTP", f"Erreur lors de l'envoi de l'email : {str(e)}")
            except Exception as e:
                # Gestion d'autres types d'erreurs
                messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
        else:
            # Si des champs sont vides
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs requis")
