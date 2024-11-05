from tkinter import *
from tkinter import filedialog, messagebox  # Ajoute messagebox ici

class PageRapport(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        Label(self, text="Gestion des Ouvriers", font=("Arial", 24)).pack(pady=20)
