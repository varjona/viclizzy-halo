import cv2
from algorithms.viclizzy_haarcascade.VicLizzy_Haarcascade import VicLizzy_Haarcascade

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
    
    Algorithm = VicLizzy_Haarcascade()
    cap = cv2.VideoCapture(0)

    while True:
        # Read in a current frame of video and make it gray.
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Capture face
        # TODO: enable multiple face capture, create detector object
        faces = Algorithm.Face_Detector(gray_frame)

        for (x, y, w, h) in faces:
            dist_face = Algorithm.Distance_Finder(w)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Drawing Text on the screen
            cv2.putText(frame, f"Distance: {dist_face:.2f} cm",
                        (x - 6, y - 6), fonts, 0.5, BLACK, 2)

        # show the frame on the screen
        cv2.imshow("frame", frame)

        # quit the program if you press 'q' on keyboard
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break
        