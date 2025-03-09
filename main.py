from .modules.ball_tracking import detect_ball
from .modules.pose_tracking import detect_foot_kick
from .modules.jersey_detection import detect_jersey
from .modules.streak_tracker import StreakTracker
from .modules.error_handler import ErrorHandler
from .modules.firebase_db import save_session, get_session
from firebase_admin import firestore
import cv2
import numpy as np
import tempfile
from fastapi import FastAPI, UploadFile, File

app = FastAPI()
streak_tracker = StreakTracker()
error_handler = ErrorHandler()

@app.post("/analyze_exercise")
async def analyze_exercise(user_id: str, file: UploadFile = File(...)):
    """Processes video to analyze kicks, detect PSV jerseys, and store session data."""
    
    # Save the uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(await file.read())
        video_path = temp_video.name

    cap = cv2.VideoCapture(video_path)
    jersey_confidences = []  # To collect jersey detection confidence scores

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_height, frame_width, _ = frame.shape
        ball_status = detect_ball(frame, frame_height)
        pose_status = detect_foot_kick(frame)

        # Update streaks and error logs
        streak_tracker.update_streak(ball_status)
        error_handler.detect_errors(ball_status, pose_status)

        # Process jersey detection:
        # Convert the current frame to JPEG bytes
        ret2, buffer = cv2.imencode(".jpg", frame)
        if ret2:
            image_bytes = buffer.tobytes()
            jersey_result = detect_jersey(image_bytes)
            if jersey_result["jersey_detected"] != "Not Detected":
                jersey_confidences.append(jersey_result["confidence"])

    cap.release()

    # Calculate average jersey confidence from all processed frames
    if jersey_confidences:
        avg_confidence = sum(jersey_confidences) / len(jersey_confidences)
    else:
        avg_confidence = 0.0

    # Categorize the jersey detection based on average confidence
    if avg_confidence > 0.75:
        jersey_detection_status = "High Confidence ✅"
    elif avg_confidence > 0.50:
        jersey_detection_status = "Average Confidence ⚠️"
    elif avg_confidence > 0.0:
        jersey_detection_status = "Low Confidence ❌"
    else:
        jersey_detection_status = "Not Detected"

    # Prepare session data
    session_data = {
        "user_id": user_id,
        "correct_kicks": streak_tracker.correct_kicks,
        "incorrect_kicks": streak_tracker.incorrect_kicks,
        "longest_streak": streak_tracker.longest_streak,
        "errors": error_handler.errors,
        "jersey_detection": {
            "status": jersey_detection_status,
            "confidence": round(avg_confidence, 2)
        },
        "timestamp": firestore.SERVER_TIMESTAMP
    }

    save_session(user_id, session_data)
    return session_data

@app.get("/session_results/{user_id}")
async def get_user_session(user_id: str):
    """Retrieves session data for a user."""
    return get_session(user_id)

