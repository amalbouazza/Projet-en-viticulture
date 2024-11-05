from tkinter import *
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PageNotifications(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Notifications", font=("Arial", 24)).pack(pady=20)

        # Champ pour le destinataire
        Label(self, text="Destinataire :").pack()
        self.destinataire_entry = Entry(self)
        self.destinataire_entry.pack()

        # Champ pour le sujet
        Label(self, text="Sujet :").pack()
        self.sujet_entry = Entry(self)
        self.sujet_entry.pack()

        # Champ pour le message
        Label(self, text="Message :").pack()
        self.message_text = Text(self, height=10, width=40)
        self.message_text.pack()

        # Bouton pour envoyer la notification
        Button(self, text="Envoyer Notification", command=self.envoyer_notification).pack(pady=20)

    def envoyer_notification(self):
        destinataire = self.destinataire_entry.get()
        sujet = self.sujet_entry.get()
        message = self.message_text.get("1.0", END).strip()

        if destinataire and sujet and message:
            try:
                # Configuration du serveur SMTP
                smtp_server = 'smtp.gmail.com'
                smtp_port = 587
                smtp_user = 'etudiant.bouazza.amal@uvt.tn'  # Remplace par ton adresse email
                smtp_password = 'Vs;({8vPC5s3'  # Utilise ton mot de passe d'application

                # Création du message
                msg = MIMEMultipart()
                msg['From'] = smtp_user
                msg['To'] = destinataire
                msg['Subject'] = sujet
                msg.attach(MIMEText(message, 'plain'))

                # Envoi de l'e-mail
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()  # Activer la sécurité
                    server.login(smtp_user, smtp_password)  # Connexion au serveur
                    server.send_message(msg)  # Envoi du message

                messagebox.showinfo("Succès", "Notification envoyée avec succès")
                # Réinitialiser les champs
                self.destinataire_entry.delete(0, END)
                self.sujet_entry.delete(0, END)
                self.message_text.delete("1.0", END)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'envoi de la notification : {str(e)}")
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs requis")
