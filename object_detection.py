from ultralytics import YOLO
import cv2
import supervision as sv


model = YOLO("yolo11n.pt")
byte_tracker = sv.ByteTrack()
annotator = sv.BoxAnnotator()

def infer_yolo11(image):
    results = model(image)
    return results

def draw_bbox(image, boxes, classes):
    assert len(boxes) > 0, "No boxes to draw"
    assert len(classes) > 0, "No classes to draw"
    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box[:4])                                                         
        label = model.names[int(cls)]
        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image

def detect_objects(frame):
#    return frame
    results = infer_yolo11(frame)
    detections = sv.Detections.from_ultralytics(results[0])
#    print(detections)
    detections = byte_tracker.update_with_detections(detections)
#    print(detections)
#    return frame
    return annotator.annotate(scene=frame.copy(), detections=detections)


