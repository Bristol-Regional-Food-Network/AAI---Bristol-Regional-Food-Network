import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import warnings
warnings.filterwarnings("ignore")

import sys
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as keras_image

from grading import (
    load_image,
    calculate_colour_score,
    calculate_size_score,
    calculate_ripeness_score,
    assign_grade,
    recommend_action
)


MODEL_PATH = "models/fruit_model.h5"


def preprocess_for_model(image_path):

    img = keras_image.load_img(image_path, target_size=(224, 224))
    img_array = keras_image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


def predict_freshness(model, image_path):

    processed = preprocess_for_model(image_path)
    rotten_probability = float(model.predict(processed, verbose=0)[0][0])

    # In your dataset: fresh = 0, rotten = 1
    fresh_probability = 1.0 - rotten_probability

    predicted_label = "fresh" if fresh_probability >= 0.5 else "rotten"

    return predicted_label, fresh_probability, rotten_probability


def grade_fresh_item(image_path, fresh_probability):

    img = load_image(image_path)

    color_score = calculate_colour_score(img)
    size_score = calculate_size_score(img)
    ripeness_score = calculate_ripeness_score(fresh_probability)

    grade = assign_grade(color_score, size_score, ripeness_score)
    action = recommend_action("fresh", grade)

    return {
        "color_score": color_score,
        "size_score": size_score,
        "ripeness_score": ripeness_score,
        "grade": grade,
        "action": action
    }


def run_pipeline(image_path):

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Train the model first."
        )

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found at {image_path}"
        )

    model = load_model(MODEL_PATH)

    predicted_label, fresh_prob, rotten_prob = predict_freshness(model, image_path)

    print("\n=== Prediction Result ===")
    print(f"Image: {image_path}")
    print(f"Predicted Label: {predicted_label}")
    print(f"Fresh Probability: {fresh_prob:.4f}")
    print(f"Rotten Probability: {rotten_prob:.4f}")

    if predicted_label == "rotten":
        action = recommend_action("rotten")
        print("\n=== Inventory Decision ===")
        print(f"Action: {action}")
        return

    results = grade_fresh_item(image_path, fresh_prob)

    print("\n=== Quality Scores ===")
    print(f"Color Score: {results['color_score']}")
    print(f"Size Score: {results['size_score']}")
    print(f"Ripeness Score: {results['ripeness_score']}")

    print("\n=== Final Assessment ===")
    print(f"Grade: {results['grade']}")
    print(f"Action: {results['action']}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python src/predict_and_grade.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    run_pipeline(image_path)


if __name__ == "__main__":
    main()