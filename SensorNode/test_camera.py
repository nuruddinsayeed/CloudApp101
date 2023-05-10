import cv2
import numpy as np
import time

import torch


API = 'http://localhost:8080/test'
MODEL_PATH = "best.pt"
# DEVICE = "cuda" if not torch.cuda.is_available() else "cpu"
DEVICE = "cpu"

def yolo2bbox(bboxes):
    xmin, ymin = bboxes[0]-bboxes[2]/2, bboxes[1]-bboxes[3]/2
    xmax, ymax = bboxes[0]+bboxes[2]/2, bboxes[1]+bboxes[3]/2
    return xmin, ymin, xmax, ymax

def plot_box(image, bboxes, labels, class_names, colors):
    # Need the image height and width to denormalize
    # the bounding box coordinates
    h, w, _ = image.shape
    for box_num, box in enumerate(bboxes):
        x1, y1, x2, y2 = yolo2bbox(box)
        # denormalize the coordinates
        xmin = int(x1*w)
        ymin = int(y1*h)
        xmax = int(x2*w)
        ymax = int(y2*h)
        width = xmax - xmin
        height = ymax - ymin
        
        class_name = class_names[int(labels[box_num])]
        
        cv2.rectangle(
            image, 
            (xmin, ymin), (xmax, ymax),
            color=colors[class_names.index(class_name)],
            thickness=2
        ) 

        font_scale = min(1,max(3,int(w/500)))
        font_thickness = min(2, max(10,int(w/50)))
        
        p1, p2 = (int(xmin), int(ymin)), (int(xmax), int(ymax))
        # Text width and height
        tw, th = cv2.getTextSize(
            class_name, 
            0, fontScale=font_scale, thickness=font_thickness
        )[0]
        p2 = p1[0] + tw, p1[1] + -th - 10
        cv2.rectangle(
            image, 
            p1, p2,
            color=colors[class_names.index(class_name)],
            thickness=-1,
        )
        cv2.putText(
            image, 
            class_name,
            (xmin+1, ymin-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            font_scale,
            (255, 255, 255),
            font_thickness
        )
    return image


class DetectAnimal():
    
    def __init__(self, model_weight_path, device) -> None:
        self.model = self.load_model(model_weight=model_weight_path)
        self.device = device
        
    def load_model(self, model_weight):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_weight, force_reload=True)
        model.conf = 0.60
        model.iou = 0.30
        return model
    
    def draw_detected_image(self, frame):
        class_names = ['Cat', 'Dog']
        colors = np.random.uniform(0, 255, size=(len(class_names), 3))
        
    def detect_animal(self, frame, class_names: list):
        self.model.to(self.device)
        results = self.model(frame)
        
        tempsum = 0.0
        tempcount = 20
        discoverymean = 0.0  # TODO: Delete this line
        
        lables, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        n = len(lables)
        
        font_scale = min(1,max(3,int(x_shape/500)))
        font_thickness = min(2, max(10,int(x_shape/50)))
        
        
        
        for i in range(n):
            animal_name = class_names[int(lables[i])]
            
            row = cord[i]
            tempcount+=1
            tempsum+=row[4].item()
            cv2.rectangle(frame,(int(row[0].item()*x_shape),int(row[1].item()*y_shape)),(int(row[2].item()*x_shape),int(row[3].item()*y_shape)),(0,0,255),2)
            cv2.putText(frame, f"{animal_name}: %0.2f" %row[4].item(), (int(row[0].item()*x_shape),int(row[1].item()*y_shape) - 10), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,255,0), font_thickness)
        if tempsum/tempcount > discoverymean:
            discoveryImage = frame
            discoverymean = tempsum/tempcount
            return discoveryImage
        return None
        


def capture_cont():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    while True:
        time.sleep(2)
        capture_success, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
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
        
        # TODO: Delete 
        animal_detector = DetectAnimal(model_weight_path=MODEL_PATH, device=DEVICE)
        
        ditected = animal_detector.detect_animal(frame=frame, class_names=['Cat', 'Dog'])
        
        if ditected is not None:
            frame = ditected
        else:
            print("Not Detected")
        
        
        if cv2.waitKey(1) == ord('q'):
            break
        
        cv2.imwrite("test.png", frame)
        break
        
    cap.release()
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    capture_cont()