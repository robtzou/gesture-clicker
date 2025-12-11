import cv2
import mediapipe as mp
import pyautogui
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# --- CONFIGURATION ---
MODEL_PATH = 'exported_model/gesture_recognizer.task'
COOLDOWN_SECONDS = 2.0  # Time to wait before triggering the same action again

# Mapping gestures to keys
# Keys must match PyAutoGUI names: https://pyautogui.readthedocs.io/en/latest/keyboard.html
GESTURE_MAP = {
    "thumbs-up": "left_click",      # back
    "peace": "left_click",    # forward
}

# --- SETUP ---
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.GestureRecognizerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO
)
recognizer = vision.GestureRecognizer.create_from_options(options)

last_action_time = 0

cap = cv2.VideoCapture(0)

print("Gesture Controller Running... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # MediaPipe needs RGB, OpenCV gives BGR
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Recognize
    # Current timestamp in milliseconds needed for VIDEO mode
    timestamp = int(time.time() * 1000)
    result = recognizer.recognize_for_video(mp_image, timestamp)

    if result.gestures:
        # Get the top-rated gesture
        top_gesture = result.gestures[0][0]
        name = top_gesture.category_name
        score = top_gesture.score

        # Only trigger if confidence is high (> 60%) and cooldown has passed
        if score > 0.6:
            current_time = time.time()
            if current_time - last_action_time > COOLDOWN_SECONDS:
                
                if name in GESTURE_MAP:
                    action = GESTURE_MAP[name]
                    print(f"Detected: {name} -> Action: {action}")
                    
                    # TRIGGER THE INPUT
                    try:
                        if action == "left_click":
                            pyautogui.leftClick()
                        else:
                            pyautogui.press(action)
                        print(f"Action executed: {action}")
                    except Exception as e:
                        print(f"Failed to execute action: {e}")
                        print("Ensure terminal has Accessibility permissions in System Settings -> Privacy & Security.")
                    
                    last_action_time = current_time

            # Visual feedback on screen
            cv2.putText(frame, f"{name} ({score:.2f})", (10, 50), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the webcam feed (optional, you can run this headless later)
    cv2.imshow('Gesture Controller', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()