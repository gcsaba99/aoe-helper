import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow import keras
from tensorflow.keras import layers
import os

# Define the CNN model
model = keras.Sequential([
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(50, 50, 3)),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation="relu"),
    layers.Dense(1, activation="sigmoid")
])

# Compile the model
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])


def preprocess_image(image):
    # Resize the image to the desired dimensions
    resized_image = image.resize((50, 50))

    # Convert the image to numpy array
    image_array = np.array(resized_image, dtype=np.float32)

    # Normalize the pixel values (optional)
    normalized_image = image_array / 255.0

    return normalized_image


def load_images(folder):
    image_folder = folder
    image_files = os.listdir(image_folder)
    villager_images = []

    for file_name in image_files:
        if file_name.endswith(".png"):
            image_path = os.path.join(image_folder, file_name)
            image = Image.open(image_path)
            villager_images.append(image)

    return villager_images


x_train = []
y_train = []

# Load images of villagers and assign the label 1
villager_images = load_images('positives')
for image in villager_images:
    processed = preprocess_image(image)
    x_train.append(processed)
    y_train.append(1)

# Load images of non-villagers and assign the label 0
non_villager_images = load_images('negatives')
for image in non_villager_images:
    processed = preprocess_image(image)
    x_train.append(processed)
    y_train.append(0)

# Convert the lists to numpy arrays
x_train = np.array(x_train)
y_train = np.array(y_train)

# Train the model
model.fit(x_train, y_train, batch_size=64, epochs=20)

model.save('model.h5')
