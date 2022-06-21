import cv2
from algorithms.viclizzy_haarcascade.VicLizzy_Haarcascade import VicLizzy_Haarcascade

if __name__ == "__main__":
    Algorithm = VicLizzy_Haarcascade()
    cap = cv2.VideoCapture(0)

    while True:
        # Read in a current frame of video and make it gray.
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Capture face
        # TODO: enable multiple face capture, create detector object
        front_faces = Algorithm.front_face_detector.detectMultiScale(gray_frame, 1.3, 5)

        if len(front_faces) != 0:
            position_list = Algorithm.Get_Front_Face_Position(frame, front_faces)
            print(position_list)
            #TODO:
            # id = Object_Tracker()
            # Send_Data_To_Flask(id, position_x, position_y)

        # show the frame on the screen
        cv2.imshow("frame", frame)

        # quit the program if you press 'q' on keyboard
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break
