from ultralytics import YOLO
import cv2


model = YOLO("yolo11n.pt")

def infer_yolo11(image):
    results = model(image)
    boxes, classes = [], []

    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()

    return boxes, classes

def draw_bbox(image, boxes, classes):
    assert len(boxes) > 0, "No boxes to draw"
    assert len(classes) > 0, "No classes to draw"
    print(boxes)
    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box[:4])                                                         
        label = model.names[int(cls)]
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

def detect_objects(frame):
    boxes, classes = infer_yolo11(frame)
    if len(boxes) > 0:
        image = draw_bbox(frame, boxes, classes)
    else:
        return frame
    return image


