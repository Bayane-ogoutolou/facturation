# facturation_app/src/utils.py
import os
import platform

def clear_screen():
    """Efface l'écran de la console de manière cross-platform"""
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')