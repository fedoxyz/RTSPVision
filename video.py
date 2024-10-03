import time
import cv2
from collections import deque
from object_detection import detect_objects
import object_detection

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
            cv2.putText(frame, f"FPS: {fps:.2f}", (10, 70), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame

    return show_fps

def create_ping_counter():
    def show_ping(frame, start_time):
        ping = (time.time() - start_time) * 1000
        cv2.putText(frame, f"Ping: {ping:.2f} ms", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return frame

    return show_ping

def start_video(url):
    show_fps = create_fps_counter()
    show_ping = create_ping_counter()
    
    cap = cv2.VideoCapture(url)
    
    while True:
        start_time = time.time()
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        frame = show_ping(frame, start_time)
        frame = show_fps(frame)
        image = detect_objects(frame) 
        cv2.imshow("Camera Stream", image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
