import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import warnings
warnings.filterwarnings("ignore")

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    precision_score,
    recall_score,
    f1_score,
)
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator


MODEL_PATH = "models/fruit_model.h5"
DATASET_PATH = "dataset"
RESULTS_DIR = "results"
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 42


def ensure_directories() -> None:
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)


def load_test_data():
    """
    Load evaluation data from the dataset folder.

    Current project setup uses a single dataset folder with a validation split.
    This evaluates on the validation subset as a temporary test proxy.
    In a production scenario, we would ideally have a separate test set that is
    not used at all during training or validation to get an unbiased evaluation.
    """
    
    datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        validation_split=0.2,
    )

    test_data = datagen.flow_from_directory(
        DATASET_PATH,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="binary",
        subset="validation",
        shuffle=False,
        seed=SEED,
    )

    print("Class labels:", test_data.class_indices)
    return test_data


def evaluate_model(model, test_data) -> dict:
    """
    Run model predictions and compute evaluation metrics.
    """
    y_true = test_data.classes

    y_prob = model.predict(test_data, verbose=1).ravel()
    y_pred = (y_prob >= 0.5).astype(int)

    metrics = {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1_score": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
    }

    report = classification_report(
        y_true,
        y_pred,
        target_names=list(test_data.class_indices.keys()),
        zero_division=0,
    )

    cm = confusion_matrix(y_true, y_pred)

    return {
        "metrics": metrics,
        "classification_report": report,
        "confusion_matrix": cm,
        "y_true": y_true,
        "y_pred": y_pred,
        "y_prob": y_prob,
    }


def save_metrics(metrics: dict) -> None:
    output_path = os.path.join(RESULTS_DIR, "metrics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
    print(f"Saved metrics to {output_path}")


def save_classification_report(report: str) -> None:
    output_path = os.path.join(RESULTS_DIR, "classification_report.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Saved classification report to {output_path}")


def save_confusion_matrix(cm: np.ndarray, class_names: list[str]) -> None:
    output_path = os.path.join(RESULTS_DIR, "confusion_matrix.png")

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
    disp.plot(cmap="Blues", values_format="d")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

    print(f"Saved confusion matrix to {output_path}")


def print_summary(metrics: dict, report: str) -> None:
    print("\n=== Evaluation Metrics ===")
    for key, value in metrics.items():
        print(f"{key.capitalize()}: {value:.4f}")

    print("\n=== Classification Report ===")
    print(report)


def main() -> None:
    ensure_directories()

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Train the model first."
        )

    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(
            f"Dataset folder not found at {DATASET_PATH}."
        )

    print("Loading model...")
    model = load_model(MODEL_PATH)

    print("Loading evaluation data...")
    test_data = load_test_data()

    print("Running evaluation...")
    results = evaluate_model(model, test_data)

    save_metrics(results["metrics"])
    save_classification_report(results["classification_report"])
    save_confusion_matrix(
        results["confusion_matrix"],
        list(test_data.class_indices.keys()),
    )

    print_summary(results["metrics"], results["classification_report"])


if __name__ == "__main__":
    main()