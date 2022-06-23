#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:58:08 2022

@author: victorarjona
"""
import cv2
import yaml
import math

class VicLizzy_Haarcascade():
    def __init__(self):
        # TODO: instead of having to use PyYAML to parse variables, just
        #   make a Python script that loads these variables/values.
        # "configs" won't be used afterwards, so might as well not even put
        # self.        
        with open("algorithms/viclizzy_haarcascade/configs/configs.yml") as file:
            configs = yaml.safe_load(file)
        
        # This algorithm uses the detector, constructed using the Haarcascade
        # file.
        self.BLACK = eval(configs["BLACK"])
        self.fonts = cv2.FONT_HERSHEY_COMPLEX
        self.cascade_classifier_location = configs["haarcascade_files_path"]
        self.front_face_detector = cv2.CascadeClassifier(self.cascade_classifier_location + configs["face_detector_xml"])
        self.profile_detector = cv2.CascadeClassifier(self.cascade_classifier_location + configs["profile_detector_xml"])
        
        # We use a reference image to generate an important value
        # ("focal_length") that'll be referenced throughout the execution.
        self.ref_image_location = configs["ref_imgs_path"] + configs["ref_img"]
        self.known_width = configs["known_width"]
        self.known_distance = configs["known_distance"]
        self.ref_image_face = self.front_face_detector.detectMultiScale(cv2.imread(self.ref_image_location))
        self.ref_image_face_width = self.ref_image_face[0][2]
        self.focal_length = self.Focal_Length_Finder(self.known_distance,
                                                     self.known_width,
                                                     self.ref_image_face_width)
    
    def Focal_Length_Finder(self, measured_distance, real_width, width_in_rf_image):
        focal_length = (width_in_rf_image*measured_distance)/real_width
        return focal_length
    
    def Distance_Finder(self, face_width_in_frame):
        """
        Utilizes the variables "known_width" and "focal_length" from the
        "configs" file. The values are used to estimate the distance to an
        object, in this case, "face_width_in_frame".
        """
        distance = (self.known_width*self.focal_length)/face_width_in_frame
        return distance

    def Position_Finder(self, distance_to_face, x_lower_left_corner):
        """
        Utilizes the variables "distance_to_face" and "face_x" coming from Run_Halo.py.
        The values are used to estimate the x and y position of a face object.
        """
        angle = x_lower_left_corner / 8
        position_x = distance_to_face * math.sin(math.radians(angle))
        position_y = distance_to_face * math.cos(math.radians(angle))

        return round(position_x, 2), round(position_y, 2)

    def Get_Front_Face_Position(self, frame, faces):
        """
        """
        positions = []
        for (x, y, w, h) in faces:
            distance_to_face = self.Distance_Finder(w)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Getting face object position
            position_x, position_y = self.Position_Finder(distance_to_face, x+w/2)
            positions.append((position_x, position_y))

            # Drawing Text on the screen
            cv2.putText(frame,
                        f"X: {position_x} cm\n Y: {position_y} cm\nDist: {distance_to_face}", (x - 6, y - 6), self.fonts, 0.5, self.BLACK, 2)

        return positions
