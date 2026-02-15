import cv2
import mediapipe as mp
import numpy as np

from Core.drowsiness import DrowsinessDetector
from Core.alarm import Alarm


# ===============================
# Initialize Core Modules
# ===============================
detector = DrowsinessDetector()
alarm = Alarm()



# ===============================
# Camera Stream (UPDATE IP IF NEEDED)
# ===============================
#url = "http://ip_address/video"
cap = cv2.VideoCapture(url)


# ===============================
# MediaPipe Setup
# ===============================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye and Mouth Landmark Indices
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = [78, 13, 14, 308]


# ===============================
# Main Loop
# ===============================
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    state = "NO FACE"

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape
        mesh_points = np.array([
            [int(p.x * w), int(p.y * h)]
            for p in face_landmarks.landmark
        ])

        # Extract Eye Points
        left_eye = mesh_points[LEFT_EYE]
        right_eye = mesh_points[RIGHT_EYE]

        # Extract Mouth Points
        mouth = mesh_points[MOUTH]

        # Calculate EAR & MAR
        left_EAR = detector.calculate_EAR(left_eye)
        right_EAR = detector.calculate_EAR(right_eye)
        EAR = (left_EAR + right_EAR) / 2.0

        MAR = detector.calculate_MAR(mouth)

        # Update Detector State
        state = detector.update(EAR, MAR)

        # Alarm Logic
        if state == "DROWSY" or state == "HIGH_FATIGUE":
            alarm.start()
        else:
            alarm.stop()

        # Draw Eye & Mouth
        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
        cv2.polylines(frame, [mouth], True, (255, 0, 0), 1)

        # Display EAR & MAR
        cv2.putText(frame, f"EAR: {EAR:.2f}", (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.putText(frame, f"MAR: {MAR:.2f}", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    else:
        alarm.stop()

    # Display Driver State
    if state == "ALERT":
        color = (0, 255, 0)
    elif state == "DROWSY":
        color = (0, 165, 255)
    elif state == "HIGH_FATIGUE":
        color = (0, 0, 255)
    else:
        color = (200, 200, 200)

    cv2.putText(frame, f"STATE: {state}", (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

    cv2.imshow("Driver Safety App Engine", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

