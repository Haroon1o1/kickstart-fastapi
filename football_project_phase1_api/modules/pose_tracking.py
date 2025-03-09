#pose_tracking.py

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def detect_foot_kick(frame):
    """Detects if only feet are used to kick the ball."""
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark

        # Get key points
        left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]
        right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]

        # Ensure the movement is from the foot, not the knee or other body parts
        foot_kick_detected = (
            left_foot.y < left_knee.y and left_foot.y < left_hip.y or
            right_foot.y < right_knee.y and right_foot.y < right_hip.y
        )

        if foot_kick_detected:
            return "Valid Foot Kick ✅"
        else:
            return "Invalid Kick ❌ (Non-Foot Movement)"

    return "No Movement Detected"

