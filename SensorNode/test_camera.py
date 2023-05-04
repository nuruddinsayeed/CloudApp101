import cv2
import numpy as np
import time


def capture_cont():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        time.sleep(2)
        capture_success, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        kernel = np.array([[-1,-1,-1,-1,-1],
                          [-1,2,2,2,-1],
                          [-1,2,8,2,-1],
                          [-1,2,2,2,-1],
                          [-1,-1,-1,-1,-1]]) / 8.0 # Guassian filter for edge enhancement
        # kernel = np.array([[-1,-1,-1], 
        #                [-1, 9,-1],
        #                [-1,-1,-1]])
        
        frame = cv2.filter2D(frame, -1, kernel)
        
        # cv2.imshow("Frame", frame)
        
        
        if cv2.waitKey(1) == ord('q'):
            break
        
        cv2.imwrite("test.png", frame)
        break
        
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    capture_cont()