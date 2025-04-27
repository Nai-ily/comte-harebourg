import pyautogui
import time

print("👉 Il faut  capturer la zone de texte du % de vie sur le coeur")
print("/!\ il faut garder la fenêtre du terminal en fenêtre active (ne pas cliquer sur la fenêtre de dofus)")
print("- Mets ta souris sur le COIN HAUT GAUCHE du % de vie")
print("- Appuie sur ENTRÉE")

input("Appuie sur ENTRÉE pour capturer le haut gauche du coeur...")
x1, y1 = pyautogui.position()
print(f"🖱️ Coin haut gauche capturé : ({x1}, {y1})")

time.sleep(1)

print("\n👉 Maintenant :")
print("- Mets ta souris sur le COIN BAS DROIT du coeur")
print("- Appuie sur ENTRÉE")

input("Appuie sur ENTRÉE pour capturer la 2e position...")
x2, y2 = pyautogui.position()
print(f"🖱️ Coin bas droit capturé : ({x2}, {y2})")

# Calcul largeur / hauteur
width = x2 - x1
height = y2 - y1

print("\n🎯 Voici ton LIFE_BAR_REGION prêt à copier-coller :")
print(f"LIFE_BAR_REGION = ({x1}, {y1}, {width}, {height})")
