#ball_tracking.py

import cv2
import numpy as np
import tempfile

def detect_ball(frame, frame_height):
    """Detect ball and validate kicks."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 168], dtype=np.uint8)
    upper_white = np.array([172, 111, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        ball_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(ball_contour)
        if radius > 5:
            knee_height = frame_height * 0.6
            kick_status = "Valid Kick ✅" if y < knee_height else "Invalid Kick ❌"
            return kick_status
    return "No Kick Detected"

def process_video(file_bytes):
    """Process uploaded video file and return kick analysis."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(file_bytes)
        video_path = temp_video.name

    cap = cv2.VideoCapture(video_path)
    results = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_height = frame.shape[0]
        kick_status = detect_ball(frame, frame_height)
        results.append(kick_status)

    cap.release()
    return {"kick_analysis": results}

