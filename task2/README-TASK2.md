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
├── data/                 # Raw dataset (gitignored)
├── dataset/              # Processed dataset
├── models/               # Trained models
├── results/              # Evaluation outputs
├── logs/                 # Prediction logs
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

## Flask AI Inference Service

To support integration with the DESD system, the AI model can be run as a lightweight Flask-based inference service.

This service:
- receives an uploaded fruit or vegetable image
- runs the trained prediction and grading pipeline
- returns a JSON response containing:
  - predicted label
  - freshness probabilities
  - colour, size, and ripeness scores
  - final grade
  - recommended action
  - explanation text

This allows the AI component to be deployed separately from the DESD web application while still being integrated into the wider system.

## Running the Flask Service

Before running the AI service, make sure the Python virtual environment is activated and all dependencies are installed.

### Start the Flask AI service

```bash
python ai_service.py
```
The service will start on: `http://127.0.0.1:5001`
This service must be running before DESD attempts to send images for AI inspection.

### Make sure to update the DESD Build
```bash
docker compose down
docker compose build --no-cache
docker compose up
```

---

## Running the Full Pipeline

### Step 1: Prepare dataset
```bash
python src/dataset_cleaner.py
```
This restructures the dataset into:
- fresh
- rotten

### Step 2: Train the model
```bash
python src/train_model.py
```
This will:
- Train the MobileNetV2 Model
- Save it to models/
- Generate training graoh

### Step 3: Evaluate the model
```bash
python src/evaluate_model.py
```
This will compute accuracy, precision, recall, and F1-score, generate a confusion matrix and save results in the results/ folder

### Step 4: Run prediction and grading
```bash
python src/predict_and_grade.py [image_path]
```
This will generate the predictions and the grade for the image and will save it and then output it

### Example Output
```bash
python src/predict_and_grade.py dataset/fresh/0a0a25fe-d5c8-4894-850a-0b9fcf5090bc.png
```
```markdown
=== Prediction Result ===
Image: dataset/fresh/0a0a25fe-d5c8-4894-850a-0b9fcf5090bc.png
Predicted Label: fresh
Fresh Probability: 0.5612
Rotten Probability: 0.4388

=== Quality Scores ===
Colour Score: 80.1
Size Score: 100.0
Ripeness Score: 56.12

=== Final Assessment ===
Grade: C
Action: Apply discount or manual review

=== Explanation ===
- Grade C was assigned because one or more features fell below the minimum Grade B thresholds.
- Ripeness score 56.12 is below the Grade B threshold (65).
```
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
The train_model.py script implements the first stage of the quality assessment pipeline. The final model uses transfer learning with MobileNetV2 to classify produce as fresh or rotten.

MobileNetV2 was selected because:
- it is pre-trained on ImageNet
- it extracts strong visual features
- it performs well on smaller datasets
- it reduces training time compared to training from scratch

The convolutional base was frozen, and only the classification layers were trained on the produce dataset.

This stage functions as an initial filtering mechanism: items predicted as rotten are removed from inventory, while fresh items proceed to the grading stage.

### Explaination for Demo
This script trains our computer vision model using transfer learning. We first classify produce as fresh or rotten using MobileNetV2. Rotten produce can be removed immediately, while fresh produce continues to the later grading stage where we assess quality in more detail using attributes like colour, size, and ripeness.


### Training Pipeline
- load the image dataset
- preprocess and normalise images
- use MobileNetV2 as a feature extractor
- train classification layers for fresh vs rotten prediction
- evaluate model performance
- save trained model and training graph

The model training pipeline was implemented in Python using TensorFlow and Keras. TensorFlow was used to define and train the convolutional neural network, while Matplotlib was used to visualise training performance.

### Loading Data

The dataset was loaded using Keras’ ImageDataGenerator, which enabled automated preprocessing and splitting of the dataset into training and validation subsets. Pixel values were normalised to the range 0–1 by dividing by 255, which improves numerical stability during training. A validation split of 20% was used so that model performance could be measured on unseen data during training. All images were resized to 224 × 224 pixels to ensure consistent input dimensions.

The folder-based dataset structure allowed class labels to be assigned automatically, with fresh produce mapped to one class and rotten produce mapped to the other.

### Building the Model

The model was built using MobileNetV2 with transfer learning.
The pre-trained convolutional base was used to extract visual features such as texture, colour, and surface patterns. This base was frozen during initial training.

Custom classification layers were added on top, including:
- a global average pooling layer
- a dense layer
- a sigmoid output layer for binary classification

The model was compiled using:
- Adam optimiser
- binary cross-entropy loss
- accuracy as the primary metric

### Training the model

The baseline CNN was trained using the training subset of the dataset, while performance on the validation subset was monitored after each epoch.
Training was initially performed for five epochs to establish a working baseline and to observe whether the model could learn meaningful distinctions between fresh and rotten produce without tuning.

### Using Transfer Learning

To improve baseline performance, transfer learning was applied using MobileNetV2 pre-trained on ImageNet. The original classification head was removed and replaced with task-specific dense layers for binary classification. The pre-trained convolutional base was frozen during initial training so that previously learned visual features could be reused while only the new classification layers were trained on the produce dataset.

### Evaluating the model

After training, the model was evaluated on the validation set to assess its ability to generalise to unseen images. Validation accuracy was used as an initial performance indicator because it provides a clearer measure of practical usefulness than training accuracy alone.

### Saving the model

The trained model was saved to file so that it could be reused without retraining. This supports reproducibility and future integration into the application.

### Plotting the results

Training and validation accuracy were plotted across epochs to provide a visual representation of the model’s learning behaviour. This made it possible to identify whether performance improved consistently and whether there were early signs of overfitting.


---

## Model Evaluation

The model was evaluated using the validation subset of the dataset to assess performance on unseen data.

The following metrics were used:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

These metrics provide a more complete evaluation than accuracy alone, particularly in understanding misclassifications.

All evaluation outputs are saved in the `results/` folder, including:
- classification report
- confusion matrix
- metric summary

This evaluation demonstrates the effectiveness of the model and highlights areas for improvement.

---

## Grading Fruit

As the dataset did not provide labelled measurements for colour, size, or ripeness, these attributes were approximated using derived image-based features. Colour quality was estimated from saturation and brightness, size was estimated from visible object area, and ripeness was approximated using the output confidence of the freshness classifier.

The system combines machine learning and rule-based logic to form a hybrid decision-making pipeline. A deep learning model is first used to classify produce as fresh or rotten. Fresh items are then evaluated using image-derived features, including colour, size, and ripeness, which are combined using rule-based thresholds to produce an interpretable quality grade and actionable recommendation.

### Calculating Colour Score

The colour quality of produce was estimated using the HSV colour space. Saturation and brightness were used as key indicators of visual quality, as fresh produce typically exhibits strong, vivid colours and sufficient brightness, whereas lower-quality or deteriorating produce tends to appear dull or dark. A weighted combination of saturation (60%) and brightness (40%) was used to compute a colour score, which was then normalised to a percentage scale (0–100). This approach provides a simple but effective proxy for visual freshness.

### Calculating Size Score

The initial size-scoring method used only the largest detected contour, which caused close-up images of single fruits to receive very high scores while images containing multiple smaller items often received disproportionately low scores. To address this, the method was revised to use the total contour area across all detected produce regions. This produced a more balanced estimate of visible produce area within the image and improved robustness for images containing multiple items.

Size was approximated using contour-based segmentation. After converting the image to grayscale and applying thresholding, contours corresponding to visible produce regions were detected. Rather than relying only on the largest contour, the total area of all detected contours was used to estimate the apparent size of the produce within the image. This value was normalised relative to the full image area to obtain a score between 0 and 100.

### Calculating Ripeness

The ripeness score was derived from the output of the trained classification model. The model produces a probability indicating how likely the produce is to be fresh. This probability was scaled to a percentage to represent a ripeness score. This approach leverages the model’s learned visual features, such as texture, discolouration, and surface irregularities, making it a strong proxy for overall freshness and condition.

### Assigning a Grade

The final quality grade was determined using a rule-based system based on predefined thresholds for colour, size, and ripeness.
Grade A represents high-quality produce meeting all upper thresholds, Grade B represents acceptable but lower-quality produce, and Grade C represents produce that may require urgent action. This rule-based approach ensures transparency and interpretability in the decision-making process.

### Recommendation System

Based on the assigned grade, the system generates actionable recommendations for producers. Rotten produce is automatically flagged for removal, while fresh produce is assigned actions based on quality grade.
This supports efficient inventory management and reduces manual decision-making.

### Testing Grading

Initial colour scoring produced consistently low values because whole-image averages were heavily influenced by shadows and background pixels. To improve robustness, the scoring function was adjusted to use a more suitable scaling range and, where appropriate, to ignore very dark pixels likely to belong to the background. This produced more meaningful colour scores across the dataset while preserving relative variation between images.

---

## Prediction and Grading Pipeline

The full prediction pipeline was implemented to combine the freshness classifier and the rule-based grading system into a single workflow. When an image is provided, the trained model first predicts whether the produce is fresh or rotten. Rotten items are immediately flagged for removal. Fresh items are then passed to a second stage where colour, size, and ripeness scores are computed and used to assign an overall grade and inventory recommendation.

End-to-end testing showed that the pipeline could successfully differentiate between rotten items, high-quality fresh items, and lower-scoring fresh items. However, the colour feature remained sensitive to lighting conditions and image composition, causing some fresh items with darker or less vivid appearance to receive lower grades. This limitation reflects the challenge of using image-derived proxy features in unconstrained real-world conditions.

---

## Prediction Logging and Monitoring

To support monitoring and future model improvement, a logging mechanism was implemented to record all prediction results.

Each time the prediction pipeline is executed, the system logs key information including:

- timestamp
- image path
- predicted label (fresh or rotten)
- prediction probabilities
- assigned grade
- recommended action

This information is stored in a CSV file located at: `logs/predictions.csv`


### Purpose of Logging

This logging functionality supports several key aspects of the system:

- **Model Monitoring:** Allows tracking of prediction trends over time
- **Error Analysis:** Helps identify incorrect predictions and edge cases
- **Future Retraining:** Logged data can be used to refine and improve the model
- **System Transparency:** Provides visibility into how the system is being used

This aligns with the case study requirement that AI engineers should be able to access interaction data to improve model performance, and that administrators should have visibility of system activity.

---

### Explainability

To support transparency and trust, an explainability layer was added to the system. Because the final quality grade is determined using explicit thresholds for colour, size, and ripeness, the system can provide direct textual explanations showing which features satisfied or failed the relevant thresholds. In addition, rotten classifications are explained using the output probabilities of the freshness model. This approach provides interpretable, user-facing justifications for automated decisions without requiring specialist knowledge of deep learning internals.

---

## Limitations

Several limitations were identified:

- Colour scoring is sensitive to lighting and background conditions
- Size estimation depends on contour detection, which can be inaccurate in complex images
- Ripeness is estimated using model confidence rather than true labels
- Dataset is limited to fresh vs rotten classification only
- Model performance may degrade on unseen environments

These limitations highlight areas for future improvement, such as:
- improved segmentation techniques
- better labelled datasets
- more advanced feature extraction

---

## API Endpoint

The Flask service exposes the following endpoint:

### POST `/predict`

This endpoint accepts an image file upload and returns the AI assessment result as JSON.

### Example JSON response

```json
{
  "image_path": "temp_example.png",
  "predicted_label": "fresh",
  "fresh_probability": 0.9973,
  "rotten_probability": 0.0027,
  "colour_score": 82.89,
  "size_score": 100.0,
  "ripeness_score": 99.73,
  "grade": "A",
  "action": "Sell at full price",
  "explanation": [
    "Grade A was assigned because all quality thresholds were met.",
    "Colour score 82.89 meets the A threshold (>= 80).",
    "Size score 100.0 meets the A threshold (>= 80).",
    "Ripeness score 99.73 meets the A threshold (>= 80)."
  ]
}
```
