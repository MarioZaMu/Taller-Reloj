"""Punto de entrada: python main.py"""

import tkinter as tk

from reloj import RelojApp

if __name__ == "__main__":
    raiz = tk.Tk()
    RelojApp(raiz)
    raiz.mainloop()
