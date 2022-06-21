#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 22 14:58:08 2022

@author: victorarjona
"""
import cv2
import yaml

class VicLizzy_Haarcascade():
    def __init__(self):
        # TODO: instead of having to use PyYAML to parse variables, just
        #   make a Python script that loads these variables/values.
        # "configs" won't be used afterwards, so might as well not even put
        # self.        
        with open("algorithms/viclizzy_haarcascade/basic_algorithm_configs.yml") as file:
            configs = yaml.safe_load(file)
        
        # This algorithm uses the detector, constructed using the Haarcascade
        # file.
        self.cascade_classifier_location = configs["haarcascade_files_path"]
        self.face_detector = cv2.CascadeClassifier(self.cascade_classifier_location + configs["face_detector_xml"])
        self.profile_detector = cv2.CascadeClassifier(self.cascade_classifier_location + configs["profile_detector_xml"])
        
        # We use a reference image to generate an important value
        # ("focal_length") that'll be referenced throughout the execution.
        self.ref_image_location = configs["ref_imgs_path"] + configs["ref_img"]
        self.known_width = configs["known_width"]
        self.known_distance = configs["known_distance"]
        self.ref_image_face = self.Face_Detector(cv2.imread(self.ref_image_location))
        self.ref_image_face_width = self.ref_image_face[0][2]
        self.focal_length = self.Focal_Length_Finder(self.known_distance,
                                                     self.known_width,
                                                     self.ref_image_face_width)
    
    def Focal_Length_Finder(self, measured_distance, real_width, width_in_rf_image):
        focal_length = (width_in_rf_image*measured_distance)/real_width
        print(focal_length)
        return focal_length
    
    def Distance_Finder(self, face_width_in_frame):
        """
        Utilizes the variables "known_width" and "focal_length" from the
        "configs" file. The values are used to estimate the distance to an
        object, in this case, "face_width_in_frame".
        """
        distance = (self.known_width*self.focal_length)/face_width_in_frame
        return distance

    def Face_Detector(self, image):
        # detecting faces in the image
        return self.face_detector.detectMultiScale(image, 1.3, 5)

