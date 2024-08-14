#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy


import cv2 as cv
import numpy as np


from queue import Queue
import pygame
import threading


import time



class PythonCamera: 
    def __init__(self, device, flag):
        self.device = device 

        self.audio_files = "y2mate.com - Camera Shutter Sound Effect.mp3"
        # Set global variables
        self.numScreenShot = 4
        self.captured = False 
        self.captured_image = None
        self.write_captured_image = False
        


        # Variable for VTEAM trigger 
        self.counter_vteam =  0 
        self.vteam_flag = flag

        # Variable for countdown 
        self.duration = 5 # countdown seconds 
        self.start_time = 0 
        self.end_time = 0 

        # Varibale for screen-shot 
        self.max_alpha = 0.6 # max opacity 
        self.max_thickness = 50 # max border thickness (black frame)
        self.current_alpha = 0 
        self.current_thickness = 0 
        self.frame_rate = 30 # fps 
        self.screenshot_sound_flag = False # flag trigger camera sound 
        self.counterScreenShot = 0 
        self.numScreenShot = 4 # max number of photos taken 

        # Init camera and mp, config
        self.cap = cv.VideoCapture(self.device)

        self.cap.set(cv.CAP_PROP_FPS, 29)
        
    def main(self): 
        print("Starting camera...")

        sound_queue = Queue()
        def sound_manager():
            while True: 
                audio_file = sound_queue.get()
                self.play_sound(audio_file)
                sound_queue.task_done()

        sound_thread = threading.Thread(target=sound_manager)
        sound_thread.daemon = True
        sound_thread.start()
        
        while (self.counterScreenShot < self.numScreenShot):
            key = cv.waitKey(10)
            if key == 27:  # ESC
                break

            # Camera capture #####################################################
            ret, image = self.cap.read()
            if not ret:
                break
            image = cv.flip(image, 1)

            image = self.crop_image(image, left_crop=0, right_crop=0, bottom_crop=0, top_crop=0)
            debug_image = copy.deepcopy(image)

            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # image.flags.writeable = False

            if self.vteam_flag:
                remaining_time = self.end_time - time.time()
                if remaining_time >= 0:
                    countdown_text = "{:.1f}".format(remaining_time)
                    # Calculate progress (0 to 1) based on remaining time
                    progress = 1 - (remaining_time / self.duration)
                    self.draw_countdown(debug_image, countdown_text, progress)  # Draw countdown circle and text
                else:
                    overlay = np.ones_like(image) * 255  # White overlay (all pixels set to white)
                    # alpha values increase in each frame
                    fps = 30
                    rate_overlay_increase = (self.max_alpha/fps) * 4  
                    rate_thickness_increase = int((self.max_thickness/fps)*7)

                    cv.addWeighted(overlay, self.current_alpha, debug_image, 1 - self.current_alpha, 0, debug_image)
                    cv.rectangle(debug_image, (0, 0), (image.shape[1], image.shape[0]),
                        color=(0, 0, 0), thickness=self.current_thickness)
                    
                    if not self.screenshot_sound_flag: 
                        sound_queue.put(self.audio_files)
                        self.screenshot_sound_flag = True
                        # capture point
                        self.captured_image = debug_image
                        immmm = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                        self.captured_imageWithoutFilter = immmm
                    if self.current_alpha <= self.max_alpha and self.current_thickness <= self.max_thickness and not self.captured: 
                        self.current_alpha += rate_overlay_increase
                        self.current_thickness += rate_thickness_increase
                    else:
                        self.captured = True
                        

                    if self.captured:
                        rate_overlay_decrease = (self.current_alpha/fps)*5
                        rate_thickness_decrease = int((self.current_thickness/fps)*6)
                        # print(current_alpha >= 0 and current_thickness >= 0)
                        if round(self.current_alpha, 2) > 0 and self.current_thickness > 0:
                            self.current_alpha -= rate_overlay_decrease
                            self.current_thickness -= rate_thickness_decrease
                        else: 
                            # Restart
                            self.write_captured_image = True
                            self.counterScreenShot += 1
                            self.screenshot_sound_flag = False
                            self.captured = False
                            self.start_time = time.time()
                            self.end_time = self.start_time + self.duration
            if self.write_captured_image: 
                cv.imwrite(f"../../front_end/src/images/{self.counterScreenShot-1}.jpg", self.captured_image)
                self.write_captured_image = False
            
            yield debug_image
        
        self.cap.release()
        cv.destroyAllWindows()
        self.counterScreenShot = 0 
        self.vteam_flag = False
        yield None

    def play_sound(self, audio_file): 
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()

        # Wait for the sound to finish playing
        while pygame.mixer.music.get_busy():
            pass

    def draw_countdown(self, frame, text, progress):
        font = cv.FONT_HERSHEY_SIMPLEX
        text_size = cv.getTextSize(text, font, 3, 2)[0]
        text_size2 = cv.getTextSize(text, font, 3, 8)[0]
        
        # Calculate center coordinates for the circle and text
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        
        # Draw the countdown text (black color)
        cv.putText(frame, text, (center_x - text_size2[0]//2, center_y + text_size[1]//2),
                    font, 3, (0, 0, 0), 8, cv.LINE_AA)
        cv.putText(frame, text, (center_x - text_size[0]//2, center_y + text_size[1]//2),
                    font, 3, (255, 255, 255), 2, cv.LINE_AA)
    
    def create_framed_image(self, original_image): 
    

        # Load the PNG image (with transparency)
        overlay_image = cv.imread('./frame1.png', cv.IMREAD_UNCHANGED)
        # cv.imshow("haha", overlay_image)

        # Ensure the overlay image has an alpha channel
        if overlay_image.shape[2] != 4:
            raise ValueError("Overlay image does not have an alpha channel")

        # Resize the overlay image to match the original image, if necessary
        print(original_image.shape[1], original_image.shape[0])
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 2731)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 2050)
        self.cap.set(cv.CAP_PROP_FPS, 29)
        actual_width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        actual_height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        print(f"Width set to: {actual_width}")
        print(f"Height set to: {actual_height}")


        overlay_image = cv.resize(overlay_image, (original_image.shape[1], original_image.shape[0]))

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
        width = 2731
        height = 2050
        resized_image = cv.resize(original_image, (width, height))
        return resized_image

    def crop_image(self, image, left_crop, right_crop, top_crop, bottom_crop):
    # Read the image

        # Calculate the coordinates for cropping
        height, width = image.shape[:2]
        cropped_image = image[top_crop:height - bottom_crop, left_crop:width - right_crop]

        # Save the cropped image
        return cropped_image