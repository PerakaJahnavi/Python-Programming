from PIL import ImageOps
import pyscreenshot as ImageGrab
import pyautogui
import time
import numpy as np


class Coordinates():
    # coordinates of replay button
    replay = (473, 255)
    # coordinates of top-right corner of dinosaur
    dino = (183, 274)


def restart_game():
    # automating the replay button
    pyautogui.click(Coordinates.replay)


count = 0


def img_box():
    box = (Coordinates.dino[0] + 60, Coordinates.dino[1],
           Coordinates.dino[0] + 160, Coordinates.dino[1] + 20)
    image = ImageGrab.grab(box)

    gray_image = ImageOps.grayscale(image)

    a = np.array(gray_image.getcolors())

    print(a.sum())
    return a.sum()


def main():
    global count
    while True:
        if img_box() != 2033:
            pyautogui.press('space')
            time.sleep(0.1)
            count = 0
        else:
            count += 1
        if count >= 10:
            restart_game()


main()