import cv2
import numpy as np

# Loading Image Function
def load_image(image_path):

    # Load an image from disk using OpenCV.
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {image_path}")
    
    # Returns the image in BGR format.
    return image

# Colour Score Function
def calculate_colour_score(image):

    # Estimate a colour quality score based on saturation and brightness.
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    saturation = hsv[:, :, 1].mean()
    brightness = hsv[:, :, 2].mean()

    # Weighted raw score
    raw_score = 0.6 * saturation + 0.4 * brightness

    # Scale into a more realistic 0-100 range for this dataset
    score = (raw_score / 180) * 100
    score = max(0, min(score, 100))

    return round(float(score), 2)


# Size Score Function
def calculate_size_score(image):
    """
    Estimate size score using total visible produce area rather than only
    the largest contour.

    This makes the score more robust for images containing multiple items.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return 50.0

    # Sum all contour areas instead of only the largest
    total_area = sum(cv2.contourArea(contour) for contour in contours)

    image_area = image.shape[0] * image.shape[1]
    area_ratio = total_area / image_area

    # Scale to percentage-like score
    score = min(area_ratio * 150, 100)

    return round(float(score), 2)


# Ripeness Score Function
def calculate_ripeness_score(fresh_probability):
    # Convert the model's predicted probability of freshness into a ripeness score.
    score = fresh_probability * 100

    return round(float(score), 2)


# Grade Assignment Function
def assign_grade(color_score, size_score, ripeness_score):
    # Assign a grade (A, B, C) based on the combined scores of colour, size, and ripeness.
    if color_score >= 70 and size_score >= 70 and ripeness_score >= 70:
        return "A"
    elif color_score >= 50 and size_score >= 50 and ripeness_score >= 50:
        return "B"
    else:
        return "C"


# Action Recommendation Function
def recommend_action(predicted_label, grade=None):
    if predicted_label == "rotten":
        return "Remove from inventory"

    if grade == "A":
        return "Sell at full price"
    elif grade == "B":
        return "Apply discount"
    else:
        return "Apply discount or manual review"