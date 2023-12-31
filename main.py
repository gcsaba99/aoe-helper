import threading
import time
import pygame
import pyautogui
from pynput import keyboard
import tensorflow as tf

from utils import is_tc_queue, region_and_crops_from_size

screenshot_size = pyautogui.screenshot().size
region, crops = region_and_crops_from_size(screenshot_size)

print(f"ℹ️ Screen size is {screenshot_size}px")

# 3 = (0, 77, 200, 50)
# 1 = (0, 77, 50, 50)

img_counter = 500


pressed_keys = set()

model = tf.keras.models.load_model('model.h5')

# User Settings
manual_on_off = False
volume = 0.4

# Keybindings
combination_on_off = {keyboard.Key.shift, keyboard.Key.f11}
combination_add_tc = {keyboard.Key.shift, keyboard.Key.f12}
combination_remove_tc = {keyboard.Key.shift, keyboard.Key.f10}

# -------------

play_voice = False

number_of_town_centers = 1


def on_press(key):
    pressed_keys.add(key)
    global manual_on_off
    global img_counter
    global number_of_town_centers
    if all(k in pressed_keys for k in combination_on_off):
        manual_on_off = not manual_on_off
        icon = '🟢' if manual_on_off else '🔴'
        print(f'{icon} Toggle play voice: ' + str(manual_on_off))
    if all(k in pressed_keys for k in combination_add_tc):
        number_of_town_centers += 1
        if number_of_town_centers > 3:
            number_of_town_centers = 3
        print('ℹ️ number of Town Centers: ' + str(number_of_town_centers))
    if all(k in pressed_keys for k in combination_remove_tc):
        number_of_town_centers -= 1
        if number_of_town_centers < 1:
            number_of_town_centers = 1
        print('ℹ️ number of Town Centers: ' + str(number_of_town_centers))
    if key == keyboard.Key.f11:
        # file_path = os.path.join('positives', f'{img_counter}.png')
        # img_counter += 1
        # screenshot = pyautogui.screenshot(region=(0, 58, 36, 36))  # region=(50, 77, 50, 50)
        # screenshot.save(file_path)
        pass


def on_release(key):
    pressed_keys.discard(key)
    # Handle the key release event
    if key == keyboard.Key.esc:
        pass


def keypress_listener():
    # Create a listener for keyboard events
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )

    # Start the listener
    listener.start()

    # Keep the listener running in the background
    listener.join()


def main_loop():
    global play_voice
    global number_of_town_centers
    pygame.init()
    pygame.mixer.init()
    sound_file = "create-extra-villagers.mp3"  # Replace with the path to your sound file
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.set_volume(volume)
    number_of_town_centers = 1
    while True:
        if manual_on_off is False:
            time.sleep(0.25)
            continue

        screenshot = pyautogui.screenshot(region=region)
        play_voice = False

        slots = [screenshot.crop(crops[0]), screenshot.crop(crops[1]), screenshot.crop(crops[2])]

        for i, slot in enumerate(slots):
            if is_tc_queue(slot, model):
                pass
            else:
                if i + 1 <= number_of_town_centers:
                    print('⚠️ Missing villager for tc number ' + str(i + 1))
                    play_voice = True

            if i + 1 == number_of_town_centers:
                break

        if play_voice and manual_on_off:
            pygame.mixer.music.play()
            time.sleep(3)
        else:
            time.sleep(0.25)

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            continue


def main():
    # Start the keypress listener on a separate thread
    keypress_thread = threading.Thread(target=keypress_listener)
    keypress_thread.start()

    # Continue executing other code (e.g., playing music) on the main thread
    main_loop()


if __name__ == "__main__":
    print('-' * 50)
    print('Controls: \n')
    print('🎚️ Shift-f11: Turn it on/off\n')
    print('➕ Shift-f12: Add TC (max 3)')
    print('➖ Shift-f10: Remove TC (min 1)\n')
    print('-' * 50)

    main()
