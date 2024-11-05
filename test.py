from tkinter import *
from tkcalendar import *
import pymysql
from tkinter import ttk, messagebox

class FormMyqsl:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de viticulture")
        self.root.geometry("1920x1080+0+0")
        
        # Frame pour le menu (barre de navigation)
        self.menu_frame = Frame(self.root, bg="lightgray")
        self.menu_frame.pack(side=TOP, fill=X)
        
        # Boutons du menu
        Button(self.menu_frame, text="Accueil", command=self.show_home).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Ouvriers", command=self.show_ouvriers).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Travaux", command=self.show_travaux).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Opérations Phytosanitaires ", command=self.show_travaux).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Notifications ", command=self.show_travaux).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Rapports ", command=self.show_travaux).pack(side=LEFT, padx=10, pady=5)

        # Création des frames pour chaque page
        self.home_frame = Frame(self.root)
        self.ouvriers_frame = Frame(self.root)
        self.travaux_frame = Frame(self.root)
        
        # Affichage de la page d'accueil au démarrage
        self.show_home()
    
    # Méthodes pour afficher chaque page
    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(fill="both", expand=1)
        Label(self.home_frame, text="Bienvenue sur la page d'accueil", font=("Arial", 24)).pack(pady=20)
    
    def show_ouvriers(self):
        self.hide_all_frames()
        self.ouvriers_frame.pack(fill="both", expand=1)
        Label(self.ouvriers_frame, text="Gestion des Ouvriers", font=("Arial", 24)).pack(pady=20)
        # Ajoute ici les widgets pour gérer les ouvriers
    
    def show_travaux(self):
        self.hide_all_frames()
        self.travaux_frame.pack(fill="both", expand=1)
        Label(self.travaux_frame, text="Gestion des Travaux", font=("Arial", 24)).pack(pady=20)
        # Ajoute ici les widgets pour gérer les travaux
    
    def hide_all_frames(self):
        """Cache tous les frames pour ne laisser apparaître que la page demandée"""
        self.home_frame.pack_forget()
        self.ouvriers_frame.pack_forget()
        self.travaux_frame.pack_forget()

# Lancement de l'application
root = Tk()
app = FormMyqsl(root)
root.mainloop()
