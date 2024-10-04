import keyboard
import time
import threading
from logger import logger

def camera_controls(ptz, media_profile):
    request = ptz.create_type('ContinuousMove')
    request.ProfileToken = media_profile.token
    
    velocity = 0.5
    last_movement = None
    
    print("Controls:")
    print("Arrow keys: Move camera")
    print("z/x: Adjust speed")
    print("Q: Quit")
    
    def stop_movement():
        if last_movement:
            logger.debug("Stopping movement of camera")
            ptz.Stop({'ProfileToken': media_profile.token})
    
    while True:
        current_movement = None
        
        if keyboard.is_pressed('up'):
            current_movement = ('up', {'PanTilt': {'x': 0, 'y': velocity}})
        elif keyboard.is_pressed('down'):
            current_movement = ('down', {'PanTilt': {'x': 0, 'y': -velocity}})
        elif keyboard.is_pressed('left'):
            current_movement = ('left', {'PanTilt': {'x': -velocity, 'y': 0}})
        elif keyboard.is_pressed('right'):
            current_movement = ('right', {'PanTilt': {'x': velocity, 'y': 0}})
        
        if current_movement:
            direction, velocity_dict = current_movement
            if current_movement != last_movement:
                stop_movement()
                logger.debug(f"Moving {direction}")
                request.Velocity = velocity_dict
                ptz.ContinuousMove(request)
                last_movement = current_movement
        elif last_movement:
            stop_movement()
            last_movement = None
        
        if keyboard.is_pressed('x'):
            velocity = min(1.0, velocity + 0.1)
            logger.debug(f"Increased velocity to {velocity:.1f}")
        elif keyboard.is_pressed('z'):
            velocity = max(0.1, velocity - 0.1)
            logger.debug(f"Decreased velocity to {velocity:.1f}")
        
        if keyboard.is_pressed('q'):
            stop_movement()
            break
        
        time.sleep(0.05)  # Small delay to reduce CPU usage

def setup_camera_controls(ptz, media_profile):
    control_thread = threading.Thread(target=camera_controls, args=(ptz, media_profile))
    control_thread.daemon = True
    control_thread.start()
    logger.info("Camera controls are set")

