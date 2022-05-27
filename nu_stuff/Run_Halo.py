import cv2
from algorithms.basic_algorithm.Basic_Algorithm import Basic_Algorithm

if __name__ == "__main__":
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
    
    Algorithm = Basic_Algorithm()
    cap = cv2.VideoCapture(0)

    while True:
        # Read in a current frame of video
        _, frame = cap.read()
        
        # Capture face
        # TODO: enable multiple face capture, create detector object
        face_width_in_frame = Algorithm.Face_Finder(frame)
        
        # check if the face is zero then not
        # find the distance
        
        if face_width_in_frame !=0:
            distance = Algorithm.Distance_Finder(face_width_in_frame)
            
            # draw line as background of text
            cv2.line(frame, (30, 30), (230, 30), RED, 32)
            cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
            
            # Drawing Text on the screen
            cv2.putText(frame,
                        f"Distance: {round(distance, 2)} CM",
                        (30, 35),
                        fonts,
                        0.6,
                        GREEN,
                        2)
        
        # show the frame on the screen
        cv2.imshow("frame", frame)
        
        # quit the program if you press 'q' on keyboard
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break
        