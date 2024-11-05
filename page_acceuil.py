from tkinter import *

class PageAcceuil(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Page d'Accueil - Analyses", font=("Arial", 24)).pack(pady=20)
