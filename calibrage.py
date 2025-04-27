import pyautogui
import time
import keyboard

def calibrate_grid():
    print("\n🔵 Calibration de la grille")

    print("→ Position de la souris sur une case, puis appuie sur CTRL...")
    while True:
        if keyboard.is_pressed('ctrl'):
            time.sleep(0.2)
            origin_x, origin_y = pyautogui.position()
            print(f"✔ Case détectée à {origin_x}, {origin_y}")
            break
        time.sleep(0.05)

    print("→ Clique sur la case à 3h de ton personnage (ouest), puis appuie sur CTRL...")
    while True:
        if keyboard.is_pressed('ctrl'):
            time.sleep(0.2)
            right_x, right_y = pyautogui.position()
            print(f"✔ Case 3h détectée à {right_x}, {right_y}")
            break
        time.sleep(0.05)

    print("→ Clique sur la case 6h (sud), puis appuie sur CTRL...")
    while True:
        if keyboard.is_pressed('ctrl'):
            time.sleep(0.2)
            down_x, down_y = pyautogui.position()
            print(f"✔ Case 6h détectée à {down_x}, {down_y}")
            break
        time.sleep(0.05)

    # Calcul
    cell_width = right_x - origin_x
    cell_height = down_y - origin_y

    print("\n📏 Résultats de calibration :")
    print(f"GRID_ORIGIN = ({origin_x}, {origin_y})")
    print(f"CELL_WIDTH = {cell_width}")
    print(f"CELL_HEIGHT = {cell_height}")

    return (origin_x, origin_y), cell_width, cell_height

if __name__ == "__main__":
    calibrate_grid()
