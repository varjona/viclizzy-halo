import cv2, requests, json, time
from algorithms.viclizzy_haarcascade.VicLizzy_Haarcascade import VicLizzy_Haarcascade

def Send_Data_To_Flask(dist, debug=True):
    url = "http://192.168.0.100:5000/data"
    dummy_id = 1
    color = "RED"
    data = [{"id": dummy_id,
             "position": [0, dist],
             "color": color}]
    json_object = json.dumps(data, indent = 4)
    
    if debug:
        print(json_object)
    
    requests.put(url, json = json_object)

if __name__ == "__main__":
    Algorithm = VicLizzy_Haarcascade()
    cap = cv2.VideoCapture(0)

    while True:
        # Read in a current frame of video and make it gray.
        _, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Capture face
        front_faces = Algorithm.front_face_detector.detectMultiScale(gray_frame, 1.3, 5)    
        if len(front_faces) != 0:
            position_list = Algorithm.Get_Front_Face_Position(frame, front_faces)
            
            dist = Algorithm.Distance_Finder(front_faces[-1][3])
            
            #print(position_list)
            #TODO:
            # id = Object_Tracker()
            try:
                Send_Data_To_Flask(dist)
            except:
                pass
            # show the frame on the screen
            #cv2.imshow("frame", frame)
        
        time.sleep(0.1)
        
        if cv2.waitKey(1) == ord("q"):
            cap.release()
            cv2.destroyAllWindows()
            break