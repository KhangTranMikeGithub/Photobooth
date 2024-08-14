import cv2
import numpy as np

def swirl_filter(image, strength=0.5, radius=None, center=None):
    if center is None:
        center = (image.shape[1] // 2, image.shape[0] // 2)  # Center of the image

    if radius is None:
        radius = min(center[0], center[1])

    # Create grid of coordinates
    y, x = np.indices(image.shape[:2])
    x = x - center[0]
    y = y - center[1]
    distance = np.sqrt(x ** 2 + y ** 2)

    # Apply swirl transformation
    angle = strength * distance / radius
    new_x = x * np.cos(angle) - y * np.sin(angle) + center[0]
    new_y = x * np.sin(angle) + y * np.cos(angle) + center[1]

    # Interpolate pixel values
    swirled_image = cv2.remap(image, new_x.astype(np.float32), new_y.astype(np.float32), cv2.INTER_LINEAR)

    return swirled_image