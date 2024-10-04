from ultralytics import YOLO
import cv2

model = YOLO("yolo11n.pt")

def infer_yolo11(image):
    results = model.track(image, persist=True, tracker="bytetrack.yaml") 
#    results = model(image)
    return results

def draw_bbox(image, boxes, classes, track_ids):
#    assert len(boxes) > 0, "No boxes to draw"
#    assert len(classes) > 0, "No classes to draw"
    for box, in zip(boxes):
#        x1, y1, x2, y2 = map(int, box[:4])                                                         
       # label = model.names[int(cls)]
#        cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
#        cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        print("Test")
    return image

def start_object_detection():

    def detect_objects(frame):
#        print(f"{frame} - frame inside detect_objects")
        results = infer_yolo11(frame)
        
        if results[0].boxes:
            boxes = results[0].boxes.xywh.cpu()
            classes = results[0].boxes.cls.cpu().numpy()
            if classes.size == 0:
                classes = []
            if results[0].boxes.id is not None:
                track_ids = results[0].boxes.id.int().cpu().tolist()
            else:
                track_ids = []
            print(track_ids)
            frame = draw_bbox(frame, boxes, classes, track_ids)

        return frame
    return detect_objects 

#    return annotated_frame
#    detections = sv.Detections.from_ultralytics(results[0])
#    print(detections)
#    detections = byte_tracker.update_with_detections(detections)
#    print(detections)
#    return frame
#    return annotator.annotate(scene=frame.copy(), detections=detections)


