import cv2
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Path to the exported model
model_path = 'exported_model/gesture_recognizer.task'

# Initialize the Gesture Recognizer
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO
)

def main():
    with GestureRecognizer.create_from_options(options) as recognizer:
        cap = cv2.VideoCapture(0) # Use 0 for default camera
        
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        start_time = time.time()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue

            # Convert the image from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Calculate timestamp in milliseconds
            timestamp_ms = int((time.time() - start_time) * 1000)

            # Recognize gestures
            result = recognizer.recognize_for_video(mp_image, timestamp_ms)

            # Display the result
            if result.gestures:
                for gesture in result.gestures:
                    # Top gesture
                    if gesture:
                        category_name = gesture[0].category_name
                        score = gesture[0].score
                        text = f"Gesture: {category_name} ({score:.2f})"
                        
                        # Draw text on frame
                        cv2.putText(frame, text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (0, 255, 0), 2, cv2.LINE_AA)
                        print(text) # Print to console as well

            cv2.imshow('MediaPipe Gesture Recognition', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()