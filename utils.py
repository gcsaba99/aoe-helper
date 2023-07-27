
import numpy as np

from constants import RESOLUTIONS, DEFAULT_RESOLUTION



def preprocess_image(image):
    # Resize the image to the desired dimensions
    resized_image = image.resize((50, 50))

    # Convert the image to numpy array
    image_array = np.array(resized_image, dtype=np.float32)

    # Normalize the pixel values (optional)
    normalized_image = image_array / 255.0

    return normalized_image



def is_tc_queue(image, model):
    processed = preprocess_image(image)

    # Perform the prediction
    prediction = model.predict(np.expand_dims(processed, axis=0), verbose=0)

    predicted_prob = prediction[0][0]
    print(f"ℹ️ {predicted_prob:.{4}f}")
    threshold = 0.93

    if predicted_prob >= threshold:
        return True
    else:
        return False



def region_and_crops_from_size(size):

    for resolution in RESOLUTIONS.values():
        if size == resolution["size"]:
            break
    else:
        print('⚠️ This resolution is not configured, the program will probably not work.'
              f" Defaulting to {DEFAULT_RESOLUTION}.")
        resolution = RESOLUTIONS[DEFAULT_RESOLUTION]

    return resolution["region"], resolution["crops"]

