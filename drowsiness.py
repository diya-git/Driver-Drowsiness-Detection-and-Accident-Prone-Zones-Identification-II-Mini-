import numpy as np


class DrowsinessDetector:
    def __init__(self,
                 ear_threshold=0.25,
                 ear_consec_frames=30,
                 mar_threshold=0.65,
                 mar_consec_frames=20):

        # Thresholds
        self.ear_threshold = ear_threshold
        self.ear_consec_frames = ear_consec_frames
        self.mar_threshold = mar_threshold
        self.mar_consec_frames = mar_consec_frames

        # Counters
        self.eye_counter = 0
        self.yawn_counter = 0

        # State
        self.state = "ALERT"

    # -------------------------
    # EAR Calculation
    # -------------------------
    def calculate_EAR(self, eye_points):
        A = np.linalg.norm(eye_points[1] - eye_points[5])
        B = np.linalg.norm(eye_points[2] - eye_points[4])
        C = np.linalg.norm(eye_points[0] - eye_points[3])
        return (A + B) / (2.0 * C)

    # -------------------------
    # MAR Calculation
    # -------------------------
    def calculate_MAR(self, mouth_points):
        vertical = np.linalg.norm(mouth_points[1] - mouth_points[2])
        horizontal = np.linalg.norm(mouth_points[0] - mouth_points[3])
        return vertical / horizontal

    # -------------------------
    # Update State
    # -------------------------
    def update(self, EAR, MAR):

        # Eye logic
        if EAR < self.ear_threshold:
            self.eye_counter += 1
        else:
            self.eye_counter = 0

        # Yawn logic
        if MAR > self.mar_threshold:
            self.yawn_counter += 1
        else:
            self.yawn_counter = 0

        # Fatigue evaluation
        fatigue_score = 0

        if self.eye_counter >= self.ear_consec_frames:
            fatigue_score += 1

        if self.yawn_counter >= self.mar_consec_frames:
            fatigue_score += 1

        if fatigue_score == 0:
            self.state = "ALERT"
        elif fatigue_score == 1:
            self.state = "DROWSY"
        else:
            self.state = "HIGH_FATIGUE"

        return self.state
