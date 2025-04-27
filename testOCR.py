import pyautogui
import cv2
import numpy as np
import pytesseract
import time

# Obtenue via "coord.py"
LIFE_BAR_REGION = (1824, 1331, 63, 32)

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- FONCTION PRINCIPALE ---
def debug_life_bar_capture():
    print("DEBUT (ESC pour leave)")

    last_print_time = time.time()

    while True:
        life_image = pyautogui.screenshot(region=LIFE_BAR_REGION)
        img = cv2.cvtColor(np.array(life_image), cv2.COLOR_RGB2GRAY)

        blurred = cv2.GaussianBlur(img, (3, 3), 0)

        zoomed = cv2.resize(blurred, None, fx=3, fy=3, interpolation=cv2.INTER_LINEAR)

        # Affiche les étapes
        cv2.imshow('Grayscale (contrast)', img)
        cv2.imshow('Zoomed (pour OCR)', zoomed)

        # OCR
        config = '--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789%'
        text = pytesseract.image_to_string(zoomed, config=config)

        # Toutes les 5 secondes ➔ afficher le texte détecté
        if time.time() - last_print_time > 5:
            print(f"Texte détecté : {text.strip()}")
            last_print_time = time.time()

        if cv2.waitKey(1) & 0xFF == 27:  # ESC pour quitter
            break

    cv2.destroyAllWindows()
    print("\n FIN")

if __name__ == "__main__":
    debug_life_bar_capture()
