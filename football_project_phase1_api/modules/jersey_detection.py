#jersey_detection.py

from ultralytics import YOLO
import cv2
import numpy as np
import tempfile

# Load the trained model
model = YOLO("best.pt")  # Ensure the trained model is in the root directory

def detect_jersey(image_bytes):
    """Detect PSV jersey and return confidence score."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        temp_image.write(image_bytes)
        image_path = temp_image.name

    # Read image using OpenCV
    img = cv2.imread(image_path)

    # Run YOLO model for jersey detection
    results = model(img)

    for result in results:
        for box in result.boxes.data:
            confidence = float(box[4])  # Confidence score

            if confidence > 0.75:
                return {"jersey_detected": "High Confidence ✅", "confidence": confidence}
            elif confidence > 0.50:
                return {"jersey_detected": "Average Confidence ⚠️", "confidence": confidence}
            else:
                return {"jersey_detected": "Low Confidence ❌", "confidence": confidence}

    return {"jersey_detected": "Not Detected", "confidence": 0.0}

