# AAI---Bristol-Regional-Food-Network

## Task 2 Overview

This project implements an AI-driven system for assessing the quality of fruits and vegetables as part of the Bristol Regional Food Network case study. The goal is to automate quality inspection and support producers in making inventory decisions.

The system is designed as a multi-stage pipeline:
- Freshness Classification
- Feature-Based Quality Assessment
- Grading System
- Decision Support


## Project Structure

```
AAI---Bristol-Regional-Food-Network/
│
├── src/                  # Python code
├── data/                 # Dataset (gitignored)
├── models/               # Trained models (gitignored)
├── requirements.txt      # Python dependencies
├── .gitignore
├── README.md
```

---

## Dataset

The dataset is too large to store on GitHub (4.9GB), so it must be downloaded separately.

**Download dataset here:**
[https://uweacuk-my.sharepoint.com/:f:/g/personal/philip4_thompson_live_uwe_ac_uk/IgAv6SriklQvQqdrzv6AEKHXARjRW6rAbFefRFviWUJcCvo?e=m00acF]

After downloading, place the dataset into the `data` folder


## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/Bristol-Regional-Food-Network/AAI---Bristol-Regional-Food-Network.git
cd AAI---Bristol-Regional-Food-Network
```

### 2. Create a virtual environment

```
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows:**

```
.venv\Scripts\activate
```

**Mac/Linux:**

```
source .venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Download the dataset

Download from the OneDrive link and place it inside the `data/` folder.

---

## Dataset Preprocessing and Structuring

The original dataset was organised into multiple folders based on both fruit type and condition (e.g., Apple_Healthy, Banana_Rotten). However, the objective of this project is to develop a system that assesses overall product quality rather than identifying specific fruit categories.

To support this, the dataset was restructured into two primary classes:
- Fresh
- Rotten

All images labelled as “Healthy” were grouped into the fresh category, while those labelled as “Rotten” were grouped into the rotten category. This restructuring was performed using a Python script that iterates through each subfolder and copies images into the appropriate category. Unique filenames were generated using UUIDs to prevent overwriting during the merging process.

This binary classification stage serves as an initial filtering mechanism within the overall system. Specifically, items classified as rotten are automatically flagged for removal from inventory, reflecting real-world handling of spoiled produce. Only items classified as fresh are passed to subsequent stages of the pipeline for further quality assessment.

Importantly, all images were retained during preprocessing, including those with varying lighting conditions, backgrounds, and orientations. This was done intentionally to preserve dataset diversity and improve the robustness of the model, enabling it to generalise more effectively to real-world scenarios where image conditions are not controlled.

---

## Rotten vs Healthy Model

### Overview for Report
The train_model.py script implements the first stage of the proposed quality assessment pipeline. Its purpose is to train a convolutional neural network to classify produce images as either fresh or rotten. This stage functions as an initial filtering mechanism: items predicted as rotten can be removed from inventory immediately, while items predicted as fresh can be passed to later stages for more detailed quality grading. The script includes dataset loading and preprocessing, CNN construction, training, validation-based evaluation, model persistence, and visualisation of training performance.

### Explaination for Demo
This script trains our baseline computer vision model. We first classify produce as fresh or rotten. Rotten produce can be removed immediately, while fresh produce continues to the later grading stage where we assess quality in more detail using attributes like colour, size, and ripeness.


### Training Pipeline
- load the image dataset
- prepare the data for learning
- build a CNN model
- train the model on fresh vs rotten images
- evaluate how well it performs
- save the trained model and graph for later use

The model training pipeline was implemented in Python using TensorFlow and Keras. TensorFlow was used to define and train the convolutional neural network, while Matplotlib was used to visualise training performance.

### Loading Data

The dataset was loaded using Keras’ ImageDataGenerator, which enabled automated preprocessing and splitting of the dataset into training and validation subsets. Pixel values were normalised to the range 0–1 by dividing by 255, which improves numerical stability during training. A validation split of 20% was used so that model performance could be measured on unseen data during training. All images were resized to 224 × 224 pixels to ensure consistent input dimensions.

The folder-based dataset structure allowed class labels to be assigned automatically, with fresh produce mapped to one class and rotten produce mapped to the other.

### Building the model

A CNN was implemented as the baseline image classification model. CNNs are well suited to image analysis because they automatically learn hierarchical visual features. The architecture consisted of three convolutional blocks with 32, 64, and 128 filters respectively, each followed by max-pooling to reduce spatial dimensions and improve computational efficiency.

After feature extraction, the output was flattened and passed through a dense layer of 128 neurons before reaching a final sigmoid output neuron for binary classification.
The model was compiled using the Adam optimiser, binary cross-entropy loss, and accuracy as the primary training metric.

### Training the model

The baseline CNN was trained using the training subset of the dataset, while performance on the validation subset was monitored after each epoch.
Training was initially performed for five epochs to establish a working baseline and to observe whether the model could learn meaningful distinctions between fresh and rotten produce without tuning.

### Evaluating the model

After training, the model was evaluated on the validation set to assess its ability to generalise to unseen images. Validation accuracy was used as an initial performance indicator because it provides a clearer measure of practical usefulness than training accuracy alone.

### Saving the model

The trained model was saved to file so that it could be reused without retraining. This supports reproducibility and future integration into the application.

### Plotting the results

Training and validation accuracy were plotted across epochs to provide a visual representation of the model’s learning behaviour. This made it possible to identify whether performance improved consistently and whether there were early signs of overfitting.

### Using Transfer Learning

To improve baseline performance, transfer learning was applied using MobileNetV2 pre-trained on ImageNet. The original classification head was removed and replaced with task-specific dense layers for binary classification. The pre-trained convolutional base was frozen during initial training so that previously learned visual features could be reused while only the new classification layers were trained on the produce dataset.

---