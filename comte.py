import pyautogui
import keyboard
import pytesseract
import time
import cv2
import numpy as np
import threading
from PIL import ImageGrab

# Config Tesseract - Il y a peut être besoin de mettre ceci en PATH sur windows (system > advanced > PATH > new) c rapide à faire
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Capturée par "calibrage.py"
CELL_WIDTH = 63
CELL_HEIGHT = 31
GRID_ORIGIN = (1184, 1008)

your_pos = None
setting_position = False

# Position de la barre de vie (capturée via "coord.py")
LIFE_BAR_REGION = (1824, 1331, 63, 32)

def get_life_percent():
    life_image = pyautogui.screenshot(region=LIFE_BAR_REGION)
    life_image = cv2.cvtColor(np.array(life_image), cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(life_image, (3, 3), 0)
    zoomed = cv2.resize(blurred, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)
    
    config = '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789%'
    text = pytesseract.image_to_string(zoomed, config=config)
    
    # Vérifier que le % de vie est bien correct - Bug entre 71% et 79%
    print(f"% de vie détecté : {text.strip()}")
    
    digits = ''.join(c for c in text if c.isdigit())
    try:
        return int(digits)
    except ValueError:
        return None


# Confusions horaires en fonction du% de vie
def get_rotation(life_percent):
    if 90 <= life_percent <= 100:
        return 90
    elif 75 <= life_percent <= 89:
        return -90
    elif 45 <= life_percent <= 74:
        return 180
    elif 30 <= life_percent <= 44:
        return -90
    elif 0 <= life_percent <= 29:
        return 90
    else:
        return 0

# Mouvement de la souris en fonction de la rotation
def rotate(direction, degrees):
    x, y = direction
    if degrees == 90:
        return y, -x
    elif degrees == -90:
        return -y, x
    elif degrees == 180:
        return -x, -y
    return x, y
    
def rotateTRUE(direction, degrees):
    x, y = direction
    if degrees == 90:
        return -y, x
    elif degrees == -90:
        return y, -x
    elif degrees == 180:
        return -x, -y
    return x, y

def grid_to_screen(pos):
    gx, gy = pos
    ox, oy = GRID_ORIGIN
    screen_x = ox + (gx - gy) * (CELL_WIDTH // 2)
    screen_y = oy + (gx + gy) * (CELL_HEIGHT // 2)
    return screen_x, screen_y


def screen_to_grid(x, y):
    ox, oy = GRID_ORIGIN
    rel_x = x - ox
    rel_y = y - oy
    gx = (rel_x / (CELL_WIDTH / 2) + rel_y / (CELL_HEIGHT / 2)) / 2
    gy = (rel_y / (CELL_HEIGHT / 2) - rel_x / (CELL_WIDTH / 2)) / 2
    return int(round(gx)), int(round(gy))


def set_player_position():
    global your_pos, setting_position
    setting_position = True
    print("\n→ Vise le fiak de ton perso et appuie sur F5, puis vise le mob et F6...")
    while setting_position:
        if keyboard.is_pressed('f5'):
            time.sleep(0.1)  # Anti double detection
            x, y = pyautogui.position()
            your_pos = screen_to_grid(x, y)
            print(f"✔ Position définie : {your_pos}")
            setting_position = False
        time.sleep(0.05)

def main_action():
    global your_pos
    if your_pos is None:
        print("⚠ Position du joueur inconnue. Appuie sur F5 d'abord.")
        return

    print("\n→ Activation du script (F6)")
    life_percent = get_life_percent()
    
    if life_percent is None:
        print("⚠ Impossible de lire le % de vie, réessaie.")
        return

    x, y = pyautogui.position()
    mouse_grid = screen_to_grid(x, y)
    dx = mouse_grid[0] - your_pos[0]
    dy = mouse_grid[1] - your_pos[1]

    # débuggage, on peux suppr cette partie
    print(f"🎯 Tu vises {mouse_grid} | Vecteur: {dx, dy}")

    rotation = get_rotation(life_percent)
    real_dx, real_dy = rotate((dx, dy), rotation)

    real_target = (your_pos[0] + real_dx, your_pos[1] + real_dy)
    screen_target = grid_to_screen(real_target)

    # débuggage, on peux suppr cette partie
    print(f"✅ Correction {rotation}° → Nouvelle case : {real_target}")
    print(f"🖱️ Déplacement souris vers {screen_target}")
    
    pyautogui.moveTo(*screen_target, duration=0.2)

def listen_hotkeys():
    keyboard.add_hotkey('f5', lambda: threading.Thread(target=set_player_position).start())
    keyboard.add_hotkey('f6', main_action)

print("🔵 Script actif : F5 = définir position | F6 = viser auto\n")
listen_hotkeys()

while True:
    time.sleep(0.1)
