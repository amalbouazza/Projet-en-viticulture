import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  # Importer ttk pour des widgets plus stylisés
from page_acceuil import PageAcceuil
from page_ouvriers import PageOuvriers
from page_travaux import PageTravaux
from page_operations import PageOperations
from page_notifications import PageNotifications
from page_rapports import PageRapport

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Gestion Viticulture")
        self.root.geometry("1200x800+100+100")
        
        # Application d'un thème de base avec ttk
        style = ttk.Style()
        style.theme_use("clam")  # Vous pouvez essayer "alt", "clam", "classic", ou un thème personnalisé

        # Définir une couleur pour l'ensemble de la fenêtre
        self.root.configure(bg="#f4f4f4")

        # Frame du menu de navigation avec un fond coloré
        self.menu_frame = tk.Frame(self.root, bg="#2d3b55")  # Couleur de fond personnalisée
        self.menu_frame.pack(side=tk.TOP, fill=tk.X)

        # Boutons du menu avec des couleurs et des polices personnalisées
        button_style = {"font": ("Arial", 12), "bg": "#4CAF50", "fg": "white", "activebackground": "#45a049", "bd": 0}
        tk.Button(self.menu_frame, text="Accueil", command=self.show_acceuil, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.menu_frame, text="Ouvriers", command=self.show_ouvriers, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.menu_frame, text="Travaux", command=self.show_travaux, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.menu_frame, text="Opérations Phytosanitaires", command=self.show_operations, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.menu_frame, text="Notifications", command=self.show_notifications, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
        tk.Button(self.menu_frame, text="Rapports", command=self.show_rapports, **button_style).pack(side=tk.LEFT, padx=10, pady=5)

        # Instanciation des pages
        self.acceuil_frame = PageAcceuil(self.root)
        self.travaux_frame = PageTravaux(self.root)
        self.ouvriers_frame = PageOuvriers(self.root, self.travaux_frame.remplir_liste_ouvriers)  # Assurez-vous que cette méthode existe dans PageTravaux
        self.operations_frame = PageOperations(self.root)
        self.notifications_frame = PageNotifications(self.root)
        self.rapports_frame = PageRapport(self.root)

        # Afficher la page d'accueil par défaut
        self.show_acceuil()

    def show_acceuil(self):
        self.hide_all_frames()
        self.acceuil_frame.pack(fill="both", expand=1)

    def show_ouvriers(self):
        self.hide_all_frames()
        self.ouvriers_frame.pack(fill="both", expand=1)

    def show_travaux(self):
        self.hide_all_frames()
        self.travaux_frame.pack(fill="both", expand=1)

    def show_operations(self):
        self.hide_all_frames()
        self.operations_frame.pack(fill="both", expand=1)

    def show_notifications(self):
        self.hide_all_frames()
        self.notifications_frame.pack(fill="both", expand=1)

    def show_rapports(self):
        self.hide_all_frames()
        self.rapports_frame.pack(fill="both", expand=1)

    def hide_all_frames(self):
        """Cache tous les frames pour ne laisser apparaître que la page demandée"""
        self.acceuil_frame.pack_forget()
        self.ouvriers_frame.pack_forget()
        self.travaux_frame.pack_forget()
        self.operations_frame.pack_forget()
        self.notifications_frame.pack_forget()
        self.rapports_frame.pack_forget()

# Exécution de l'application
root = tk.Tk()
app = Application(root)
root.mainloop()
