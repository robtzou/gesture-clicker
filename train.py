import os
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer

# 1. Define dataset path
dataset_path = "data"  # Path to your data folder created in Phase 1

# 2. Load the dataset
# This function automatically scans the folders and labels images based on folder names
data = gesture_recognizer.Dataset.from_folder(
    dirname=dataset_path,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)

# 3. Split data into Training (80%), Validation (10%), and Testing (10%)
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)

# 4. Train the model
# Using 'MobileNetV2' as base (good balance of speed/accuracy)
hparams = gesture_recognizer.HParams(export_dir="exported_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options
)

# 5. Evaluate performance
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test accuracy: {acc}")

# 6. Export the model
# This produces the 'gesture_recognizer.task' file you will use in your app
model.export_model()
print("Model exported to /exported_model/gesture_recognizer.task")