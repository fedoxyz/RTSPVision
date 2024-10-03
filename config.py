import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP")
PORT = os.getenv("PORT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
RTSP_URL = os.getenv("RTSP_URL")


