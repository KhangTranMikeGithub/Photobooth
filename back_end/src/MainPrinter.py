import cups
import cv2
import numpy as np
from PIL import Image
from MainQRcode import link_to_qrcode, uploadPhoto

def create_framed_image(original_image):
    # Load the PNG image (with transparency)
    overlay_image = cv2.imread('./IMG_3102.PNG', cv2.IMREAD_UNCHANGED)

    # Ensure the overlay image has an alpha channel
    if overlay_image.shape[2] != 4:
        raise ValueError("Overlay image does not have an alpha channel")

    # Resize the overlay image to match the original image, if necessary
    overlay_image = cv2.resize(overlay_image, (original_image.shape[1], original_image.shape[0]))

    # Split the overlay image into its color and alpha channels
    overlay_color = overlay_image[:, :, :3]
    overlay_alpha = overlay_image[:, :, 3] / 255.0  # Normalize alpha channel to be in range [0, 1]

    # Ensure the original image is in BGR format
    if original_image.shape[2] != 3:
        raise ValueError("Original image must be in BGR format")

    # Create an inverse alpha mask
    inverse_alpha = 1.0 - overlay_alpha

    # Prepare the overlay
    for c in range(0, 3):
        original_image[:, :, c] = (overlay_alpha * overlay_color[:, :, c] + inverse_alpha * original_image[:, :, c])

    return original_image



def insert_qrcode(qrcode_path, main_image, position):
    background = main_image
    overlay = cv2.imread(qrcode_path)
    side = 120
    overlay = cv2.resize(overlay, (side,side))
    overlay_x, overlay_y = overlay.shape[:2]
    print(overlay_x, overlay_y)
    # Ensure overlay has alpha channel
    if overlay.shape[2] != 4:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)

    # Define the position for the overlay
    # x, y = 50, 50
    main_y, main_x = main_image.shape[:2]
    margin = 15
    if position == "up":
        x = main_x - overlay_x - margin
        y = main_y//2 - overlay_y - margin
    elif position == "down": 
        x = main_x - overlay_x - margin
        y = main_y - overlay_y - margin


    # Resize overlay if necessary
    # overlay = cv2.resize(overlay, (100, 100))

    # Extract the region of interest (ROI) from the background image
    rows, cols, _ = overlay.shape
    roi = background[y:y+rows, x:x+cols]

    # Separate alpha channel from the overlay image
    overlay_img = overlay[:, :, :3]
    overlay_alpha = overlay[:, :, 3] / 255.0  # Normalize the alpha mask to keep values between 0 and 1

    # Blend the images using the alpha channel
    for c in range(0, 3):
        roi[:, :, c] = (1.0 - overlay_alpha) * roi[:, :, c] + overlay_alpha * overlay_img[:, :, c]

    # Put the blended region back into the background image
    background[y:y+rows, x:x+cols] = roi
    return background


def print_image(img1_path, img2_path): 
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = list(printers.keys())[0]  # Select the third available printer
    print(printer_name)

    

    # Get DPI from the first image or use the default DPI if not available

    # Convert PIL images to OpenCV format
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    # Ensure both images are in color
    if len(img1.shape) == 2:  # grayscale image
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    if len(img2.shape) == 2:  # grayscale image
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)

    # Get dimensions
    height1, width1 = img1.shape[:2]
    height2, width2 = img2.shape[:2]

    # Choose the width to resize both images to (typically the smaller width)
    min_width = min(width1, width2)

    # Resize images
    img1_resized = cv2.resize(img1, (min_width, int(height1 * min_width / width1)))
    img2_resized = cv2.resize(img2, (min_width, int(height2 * min_width / width2)))

    # Concatenate images vertically
    combined_img = cv2.vconcat([img1_resized, img2_resized])

    # Apply the overlay
    combined_img = create_framed_image(combined_img)

    # Save the combined image with the original DPI
    output_path = "combined_image.jpg"
    cv2.imwrite(output_path, combined_img)
    # combined_img = cv2.resize(combined_img, (283, 419))
    
    gg_link = uploadPhoto(output_path)
    qr_path = link_to_qrcode(gg_link, "example_qrcode1.png")


    combined_img = insert_qrcode(qr_path, combined_img, "up")
    combined_img = insert_qrcode(qr_path, combined_img, "down")
    cv2.imwrite(output_path, combined_img)
    

    # Display the combined image (optional)
    # cv2.imshow('Combined Image', combined_img)
    # # Printing
    # options = { 
    #     'media': 'Postcard'
    # }
    # conn.printFile(printer_name, output_path, "Testing1", options)    

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Print the image
