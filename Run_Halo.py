#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 15:36:16 2021

@author: sysadmin
"""
# IMPORTS ------------------------------------------------------------------- #
import cv2
import math
# IMPORTS ------------------------------------------------------------------- #
'''
Description
The vicklizzy-halo pro


TODO:
    1) Turn color image to gray to not repeat gray-scaling.
    2) There are two similar for loops: one in the while loop, and one in the
        face data function.
    3) Have a flipped image ready.
    4) Have gray image ready.
    6) Make a debug option.
'''

# Helper variables -----------------------------------------------------------#
#   Distance from camera to object(face) measured.
known_distance = 30  # Inches

#   Mine is 14.3cm something, measure your face width.
known_width = 5.7  # Inches

GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 242)
GOLDEN = (32, 218, 165)
LIGHT_BLUE = (255, 9, 2)
PURPLE = (128, 0, 128)
CHOCOLATE = (30, 105, 210)
PINK = (147, 20, 255)
ORANGE = (0, 69, 255)

fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX

# Camera Object
cap = cv2.VideoCapture(0)
_, frame = cap.read()

# Width and height of a frame (image).
x_frame_len = len(frame[1])
y_frame_len = len(frame)

# Colors  >>> BGR Format(BLUE, GREEN, RED)
distance_level = 0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output21.mp4', fourcc, 30.0, (640, 480))

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# profile_face detector object
profile_face_classifier = cv2.CascadeClassifier("haarcascade_profileface.xml")

# body detector object
body_classifier = cv2.CascadeClassifier("haarcascade_upperbody.xml")

# Reading reference image from directory
# This is for a face!
ref_image = cv2.imread("Ref_image.png")

# Helper functions -----------------------------------------------------------#


def Focal_Length(measured_distance, real_width, width_in_rf_image):
    """
    This function calculates the focal length (distance between lens to CMOS
    sensor), it is simple constant we can find by using MEASURED_DISTACE,
    REAL_WIDTH (actual width of object) and WIDTH_OF_OBJECT_IN_IMAGE.

    Paramaters:
        measured_distance   int     It is distance measured from object to the
                                    camera while capturing reference image.

        Real_Width          int     It is the actual width of object in the
                                    real world (like My face width of 5.7
                                    inches).

        Width_In_Image      int     It is object width in the frame /image in
                                    our case in the reference image(found by
                                    Face detector).

    Return:
        Focal_Length        float
    """
    focal_length = (width_in_rf_image*measured_distance)/real_width
    return focal_length


def Distance_Finder(focal_length, real_face_width, face_width_in_frame):
    """
    This function estimates the distance between the object and camera using
    the following parameters.
    Parameters:
        focal_length        float   Return parameter by the Focal_Length
                                    function.

        real_width          int     It is the actual width of object, in real world
                                    (like My face width is = 5.7 Inches).

        object_Width_Frame  int     Width of object in the image(frame in our
                                    case, using Video feed).
    Return:
        distance            float   Distance estimated.
    """
    distance = (real_face_width*focal_length)/face_width_in_frame
    return distance


def Face_Data(image, CallOut, distance_lvl):
    """
    This function Detect face and Draw Rectangle and display the distance over
    screen.

    Parameters:
        Image           Mat     Frame.

        Call_Out        bool    If want show Distance and Rectangle on the
                                Screen or not.

        distance_lvl    int     Which change the line according the Distance
                                changes(Intractivate).

    Return:
        face_width      int     It is width of face in the frame which allow us
                                to calculate the distance and find focal
                                length.

        face            list    Length of face and (face paramters).

        face_center_x   TODO    face centroid_x coordinate(x)

        face_center_y   TODO    face centroid_y coordinate(y)
    """

    face_width = 0
    # face_x, face_y = 0, 0
    face_center_x = 0
    face_center_y = 0

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

    for (x, y, w, h) in faces:
        line_thickness = 2

        # print(len(faces))
        LLV = int(h*0.12)
        # print(LLV)

        # cv2.rectangle(image, (x, y), (x+w, y+h), BLACK, 1)
        cv2.line(image, (x, y+LLV), (x+w, y+LLV), (GREEN), line_thickness)
        cv2.line(image, (x, y+h), (x+w, y+h), (GREEN), line_thickness)
        cv2.line(image, (x, y+LLV), (x, y+2*LLV), (GREEN), line_thickness)
        cv2.line(image, (x+w, y+LLV), (x+w, y+2*LLV), (GREEN), line_thickness)
        cv2.line(image, (x, y+h), (x, y+h-LLV), (GREEN), line_thickness)
        cv2.line(image, (x+w, y+h), (x+w, y+h-LLV), (GREEN), line_thickness)

        face_width = w
        # face_center = []

        # Drawing circle at the center of the face
        face_center_x = int(w/2)+x
        face_center_y = int(h/2)+y

        if distance_lvl < 10:
            distance_lvl = 10

        # cv2.circle(image, (face_center_x, face_center_y),5, (255,0,255), 3 )
        if CallOut is True:
            # cv2.line(image, (x,y), (face_center_x,face_center_y ), (155,155,155),1)
            cv2.line(image, (x, y-11), (x+180, y-11), (ORANGE), 28)
            cv2.line(image, (x, y-11), (x+180, y-11), (YELLOW), 20)
            cv2.line(image, (x, y-11), (x+distance_level, y-11), (GREEN), 18)

            # cv2.circle(image, (face_center_x, face_center_y),2, (255,0,255), 1 )
            # cv2.circle(image, (x, y),2, (255,0,255), 1 )

        # face_x = x
        # face_y = y

    return face_width, faces, face_center_x, face_center_y


def Position_Finder(distance, face_x):
    # TODO: test and find out a better number to divide face_x to get the
    #       angle.
    angle = face_x/8
    position_x = distance * math.sin(math.radians(angle))
    position_y = distance * math.cos(math.radians(angle))

    return round(position_x, 2), round(position_y, 2)


def Profile_Face_Left_Data(frame, gray_frame):
    # Pass frame to our body classifier
    profile_face_l = profile_face_classifier.detectMultiScale(gray_frame, 1.2,
                                                              5)

    # Extract bounding boxes for any bodies identified
    for (x, y, w, h) in profile_face_l:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(frame, "Left profile face found!", (x, y-2), fonts, 0.5,
                    (BLACK), 2)

    return profile_face_l


# profile_face Right detection Function
def Profile_Face_Right_Data(frame, gray_frame):
    # flipped_frame = cv2.flip(frame, 1)
    flipped_g_frame = cv2.flip(gray_frame, 1) 
    profile_face_r = profile_face_classifier.detectMultiScale(flipped_g_frame,
                                                              1.2, 5)

    # Extract bounding boxes for any bodies identified
    for (x, y, w, h) in profile_face_r:
        cv2.rectangle(frame, (x_frame_len-x-w, y), (x_frame_len-x, y+h), (0, 255, 255), 2)
        cv2.putText(frame, "Right profile face found!", (x_frame_len-x-w, y-2),
                    fonts, 0.5, (BLACK), 2)

    return profile_face_r


# body detection Function
def Body_Data(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Pass gray frame to our body classifier
    bodies = body_classifier.detectMultiScale(gray, 1.2, 5)

    # Extract bounding boxes for any bodies identified
    for (x, y, w, h) in bodies:
        cv2.rectangle(image, (x, y+20), (x+w, y+h), (0, 255, 255), 2)
        cv2.putText(image, "Upper-Body found!", (x, y-2), fonts, 0.5,
                    (BLACK), 2)

    return bodies


ref_image_face_width, _, _, _ = Face_Data(ref_image, False, distance_level)

focal_length_found = Focal_Length(known_distance, known_width,
                                  ref_image_face_width)

print(focal_length_found)

while True:
    _, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Get body data
    bodies = Body_Data(frame)

    # Get profile_face data
    # profile_face_l = Profile_Face_Left_Data(frame, gray_frame)
    # profile_face_r = Profile_Face_Right_Data(frame, gray_frame)

    # Get face data
    face_width_in_frame, Faces, _, _ = Face_Data(frame, True, distance_level)

    # finding the distance by calling function Distance finder
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame != 0:
            distance = Distance_Finder(focal_length_found, known_width,
                                       face_width_in_frame)
            distance = round(distance, 2)

            # Drawing Text on the screen
            distance_level = int(distance)
            pos_x, pos_y = Position_Finder(distance, face_x)

            #cv2.putText(frame, f"Distance {Distance} Inches", (face_x-6, face_y-6), fonts, 0.5, (BLACK), 2)
            cv2.putText(frame, f"X: {pos_x}, Y: {pos_y}",
                        (face_x - 6, face_y - 6), fonts, 0.5, (BLACK), 2)

    cv2.imshow("VicLizzy Distance Measurement", frame)
    # out.write(frame)

    if cv2.waitKey(100) == ord("q"):
        break

cap.release()
# out.release()
cv2.destroyAllWindows()

# CONTENT ------------------------------------------------------------------- #
