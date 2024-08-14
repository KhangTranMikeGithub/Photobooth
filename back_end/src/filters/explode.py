import cv2
import numpy as np
from utils import CvFpsCalc


def explode_frame(frame):
    (h, w, _) = frame.shape
    center_x = w / 2
    center_y = h / 2
    radius = 400
    amount = -0.4
    

    x_coords, y_coords = np.meshgrid(np.arange(w), np.arange(h))

    delta_x = x_coords - center_x
    delta_y = y_coords - center_y
    distance = delta_x ** 2 + delta_y ** 2
    mask = distance < (radius ** 2)

    factor = np.where(mask, np.power(np.sin(np.pi * np.sqrt(distance) / radius / 2), -amount), 1.0)

    flex_x = factor * delta_x + center_x
    flex_y = factor * delta_y + center_y

    flex_x = flex_x.astype(np.float32)
    flex_y = flex_y.astype(np.float32)

    dst = cv2.remap(frame, flex_x, flex_y, cv2.INTER_LINEAR)
   
    return dst

def main():
    cap = cv2.VideoCapture(0)
    cvFpsCalc = CvFpsCalc(buffer_len=10)
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Unable to capture frame.")
            break

        cv2.imshow('Webcam', explode_frame(frame, cvFpsCalc))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
