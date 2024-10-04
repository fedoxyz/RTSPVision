import time
import cv2
from collections import deque
from functools import reduce
from typing import Callable
from object_detection import start_object_detection

# Assume object_detection.detect_objects exists

def create_fps_counter(avg_window=30):
    start_time = time.time()
    frame_times = deque(maxlen=avg_window)
    def show_fps(frame):
#        print(f"{frame} - frame inside show_fps")
        nonlocal start_time
        current_time = time.time()
        frame_times.append(current_time - start_time)
        start_time = current_time
        if len(frame_times) > 1:
            fps = len(frame_times) / sum(frame_times)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame
    return show_fps

def create_ping_counter():
    start_time = time.time()
    def show_ping(frame):
#        print(f"{frame} - frame inside show_ping")
#        print(f"{type(frame)} - type of frame inside inner")
        ping = (time.time() - start_time) * 1000
        cv2.putText(frame, f"Ping: {ping:.2f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame
    return show_ping

def pipeline(*functions: Callable) -> Callable:
    return lambda x: reduce(lambda v, f: f(v), functions, x)

def start_video(url: str, *pipeline_functions: Callable):
    cap = cv2.VideoCapture(url)
    
    # Create the pipeline
    process_frame = pipeline(
        create_ping_counter(),
        create_fps_counter(),
        start_object_detection(),
        *pipeline_functions
    )

    while True:
        ret, frame = cap.read()
        print(type(frame))
        if not ret:
            print("Error: Could not read frame.")
            break

        # Apply the pipeline to the frame
        frame = process_frame(frame)
#        print(f"Frame type: {type(frame)}")
#        print(f"Frame name: {frame.__name__ if hasattr(frame, '__name__') else 'No name'}")
#        print(f"Frame source: {frame.__module__ if hasattr(frame, '__module__') else 'Unknown module'}")
#        print(f"Frame docs: {frame.__doc__ if hasattr(frame, '__doc__') else 'No documentation'}")
        cv2.imshow("Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
