import os.path
import threading
import time
import pygame
import pygame_menu
import pyautogui
from pynput import keyboard
import numpy as np
import tensorflow as tf
from training import preprocess_image


def is_tc_queue(image):
    processed = preprocess_image(image)

    # Perform the prediction
    prediction = model.predict(np.expand_dims(processed, axis=0), verbose=0)

    predicted_prob = prediction[0][0]
    print(predicted_prob)
    threshold = 0.93

    if predicted_prob >= threshold:
        return True
    else:
        return False


# 3 = (0, 77, 200, 50)
# 1 = (0, 77, 50, 50)
region = (0, 77, 200, 50)

img_counter = 115


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
        print('Toggle play_voice: ' + str(manual_on_off))
    if all(k in pressed_keys for k in combination_add_tc):
        number_of_town_centers += 1
        print('number of Town Centers: ' + str(number_of_town_centers))
    if all(k in pressed_keys for k in combination_remove_tc):
        number_of_town_centers -= 1
        if number_of_town_centers < 1:
            number_of_town_centers = 1
        print('number of Town Centers: ' + str(number_of_town_centers))
    if key == keyboard.Key.f11:
        file_path = os.path.join('negatives', f'{img_counter}.png')
        img_counter += 1
        screenshot = pyautogui.screenshot(region=(50, 77, 50, 50))
        screenshot.save(file_path)
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

        slots = [screenshot.crop((0, 0, 50, 50)), screenshot.crop((50, 0, 100, 50)), screenshot.crop((100, 0, 150, 50))]

        for i, slot in enumerate(slots):
            if is_tc_queue(slot):
                pass
            else:
                if i + 1 <= number_of_town_centers:
                    print('missing villager for tc number ' + str(i + 1))
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


# Start the keypress listener on a separate thread
keypress_thread = threading.Thread(target=keypress_listener)
keypress_thread.start()

# Continue executing other code (e.g., playing music) on the main thread
main_loop()
