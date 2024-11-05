from tkinter import *
from tkinter import filedialog, messagebox
from page_acceuil import PageAcceuil
from page_ouvriers import PageOuvriers
from page_travaux import PageTravaux
from page_operations import PageOperations
from page_notifications import PageNotifications
from page_rapports import PageRapport

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Application de Gestion viticulture")
        self.root.geometry("1200x800+100+100")

        # Frame du menu de navigation
        self.menu_frame = Frame(self.root, bg="lightgray")
        self.menu_frame.pack(side=TOP, fill=X)

        # Boutons du menu
        Button(self.menu_frame, text="Accueil", command=self.show_acceuil).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Ouvriers", command=self.show_ouvriers).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Travaux", command=self.show_travaux).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Opérations Phytosanitaires", command=self.show_operations).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Notifications", command=self.show_notifications).pack(side=LEFT, padx=10, pady=5)
        Button(self.menu_frame, text="Rapports", command=self.show_rapports).pack(side=LEFT, padx=10, pady=5)

        # Frame pour chaque page
        self.acceuil_frame = PageAcceuil(self.root)
        self.ouvriers_frame = PageOuvriers(self.root)
        self.travaux_frame = PageTravaux(self.root)
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
root = Tk()
app = Application(root)
root.mainloop()
