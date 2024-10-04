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
        nonlocal start_time
        current_time = time.time()
        frame_times.append(current_time - start_time)
        start_time = current_time
        if len(frame_times) > 1:
            fps = len(frame_times) / sum(frame_times)
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame
    return show_fps

def create_lattency_counter():
    last_request_time = time.time()
    
    def measure_lattency(frame):
        nonlocal last_request_time
        current_time = time.time()
        ping = (current_time - last_request_time) * 1000  # Convert to milliseconds
        
        # Update the last request time for the next frame
        last_request_time = current_time
        
        # Add ping text to the frame
        cv2.putText(frame, f"Frame processing lattency: {ping:.2f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame
    
    return measure_lattency

def pipeline(*functions: Callable) -> Callable:
    return lambda x: reduce(lambda v, f: f(v), functions, x)

def start_video(url: str, *pipeline_functions: Callable):
    cap = cv2.VideoCapture(url)
    
    # Create the pipeline
    process_frame = pipeline(
        create_fps_counter(),
        start_object_detection(),
        create_lattency_counter(),
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
        cv2.imshow("Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
