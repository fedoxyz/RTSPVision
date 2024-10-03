from controls import setup_camera_controls
import cv2
from audio import start_audio
from video import start_video
from config import IP, PORT, USERNAME, PASSWORD, RTSP_URL
from onvif import ONVIFCamera

def connect_to_camera(ip, port, user, password):
    print("Starting connection")
    try:
        mycam = ONVIFCamera(ip, port, user, password)
        media = mycam.create_media_service()
        ptz = mycam.create_ptz_service()
        imaging = mycam.create_imaging_service()
        
        profiles = media.GetProfiles()
        if not profiles:
            raise Exception("No media profiles found")
        media_profile = profiles[0]
        
        return mycam, media, ptz, imaging, media_profile
    except Exception as e:
        print(f"Error connecting to camera: {str(e)}")
        return None, None, None, None, None


def main():
    mycam, media, ptz, imaging, media_profile = connect_to_camera(IP, PORT, USERNAME, PASSWORD)
    
    setup_camera_controls(ptz, media_profile)

    start_audio(RTSP_URL)
    start_video(RTSP_URL)

if __name__ == "__main__":
    main()