from ultralytics import YOLO
import cv2
from torch import Tensor
import numpy as np
from logger import logger
from tracker.tracker import register_tracker

model = YOLO("yolo11n.pt")

#kwargs = {}
#kwargs["conf"] = kwargs.get("conf") or 0.1  # ByteTrack-based method needs low confidence predictions as input
#kwargs["batch"] = kwargs.get("batch") or 1  # batch-size 1 for tracking in videos
#kwargs["mode"] = "track"


def infer_yolo11(image, **kwargs):
    kwargs["conf"] = 0.1
    kwargs["batch"] = 1 
    kwargs["mode"] = "track"
    logger.debug("Starting inference of YOLO")
    if not hasattr(infer_yolo11, "_tracker_registered"):
        register_tracker(model, persist=True)
        infer_yolo11._tracker_registered = True
    results = model.predict(image, **kwargs)
#    results = model.track(image, persist=True, tracker="bytetrack.yaml") 
    return results

def draw_bbox(image, boxes, classes, track_ids):
    if isinstance(boxes, Tensor):
        boxes = boxes.cpu().numpy()
    elif not isinstance(boxes, np.ndarray):
        boxes = np.array(boxes)

    logger.debug("boxes{}")

    classes = classes.tolist() if isinstance(classes, Tensor) else list(classes)
    track_ids = track_ids.tolist() if isinstance(track_ids, Tensor) else list(track_ids)

    if len(boxes) == 0:
        return image

    if boxes.ndim == 1:
        boxes = boxes.reshape(1, -1)

    for i, (box, cls, track_id) in enumerate(zip(boxes, classes, track_ids)):
        if len(box) != 4:
            logger.warning(f"Skipping invalid bounding box: {box}")
            continue

        x1, y1, x2, y2 = map(int, box[:4])

        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)

        label = f"Class: {model.names[int(cls)]}, ID: {track_id}"

        label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        y_label = max(y1, label_size[1])
        cv2.rectangle(image, (x1, y_label - label_size[1] - baseline), 
                      (x1 + label_size[0], y_label + baseline), 
                      (255, 255, 255), cv2.FILLED)
        cv2.putText(image, label, (x1, y_label), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)

    return image

def start_object_detection():

    def detect_objects(frame):
        results = infer_yolo11(frame)
        
        if results[0].boxes:
            boxes = results[0].boxes.xyxy.cpu()
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



