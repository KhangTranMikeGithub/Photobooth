import cv2
import mediapipe as mp
from utils import CvFpsCalc
import numpy as np

def overlay_image(background, overlay, x, y):
    h, w, _ = overlay.shape
    if x < 0 or y < 0 or x + w > background.shape[1] or y + h > background.shape[0]:
        print("Overlay exceeds frame boundaries.")
        return background

    roi = background[y:y+h, x:x+w]
    overlay_image = overlay[:, :, :3]
    overlay_mask = overlay[:,:,3] / 255.0
    background_mask = 1.0 - overlay_mask
    for c in range(0, 3):
        roi[:, :, c] = (overlay_mask * overlay_image[:, :, c] +
                        background_mask * roi[:, :, c])
    return background

def apply_face_filter(frame, apple_img, detection_results):
    for detection in detection_results:
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = frame.shape
        bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
               int(bboxC.width * iw), int(bboxC.height * ih)
        
        new_width = bbox[2]
        new_height = int(apple_img.shape[0] * (new_width / apple_img.shape[1]))
        
        resized_apple_img = cv2.resize(apple_img, (new_width, new_height), interpolation=cv2.INTER_AREA)
        
        apple_x = bbox[0] + bbox[2] // 2 - resized_apple_img.shape[1] // 2
        apple_y = bbox[1] - resized_apple_img.shape[0]
        
        frame = overlay_image(frame, resized_apple_img, apple_x, apple_y)

    return frame


def main():
    mp_face_detection = mp.solutions.face_detection
    cap = cv2.VideoCapture(0)
    cvFpsCalc = CvFpsCalc(buffer_len=10)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    with mp_face_detection.FaceDetection(
            model_selection=1, min_detection_confidence=0.5) as face_detection:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Unable to capture frame.")
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            detection_results = []
            if results.detections:
                for detection in results.detections:
                    detection_results.append(detection)

            if detection_results:
                frame = apply_face_filter(frame, cvFpsCalc, apple_img, detection_results)

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    apple_img = cv2.imread('butterflies.png', cv2.IMREAD_UNCHANGED)
    apple_img = cv2.resize(apple_img, (150, 75))
    main()
