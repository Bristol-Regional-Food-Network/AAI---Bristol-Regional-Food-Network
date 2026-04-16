# Philip Thompson 22024226

# These lines suppress TensorFlow warnings and logs for cleaner output during training.
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import warnings
warnings.filterwarnings("ignore")

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
import matplotlib.pyplot as plt


# Data Loading Function
def load_data():
    datagen = ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_data = datagen.flow_from_directory(
        "dataset/",
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        "dataset/",
        target_size=(224, 224),
        batch_size=32,
        class_mode='binary',
        subset='validation'
    )

    print("Class labels:", train_data.class_indices)

    return train_data, val_data

# Model Building Function
def build_model():
    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )

    # Keep pretrained layers fixed for now
    base_model.trainable = False

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    return model

# Training Function
def train_model(model, train_data, val_data):
    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=5
    )
    return history

# Evaluation Function
def evaluate_model(model, val_data):
    loss, acc = model.evaluate(val_data)
    print(f"Validation Accuracy: {acc:.4f}")

# Model Saving Function
def save_model(model):
    model.save("models/fruit_model.h5")
    print("Model saved to models/fruit_model.h5")

# Visualization Function
def plot_results(history):
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title("Training Performance")
    plt.savefig("models/training_graph.png")
    plt.show()

# Main Function
def main():
    train_data, val_data = load_data()
    model = build_model()
    history = train_model(model, train_data, val_data)
    evaluate_model(model, val_data)
    save_model(model)
    plot_results(history)


# Run Point
if __name__ == "__main__":
    main()
