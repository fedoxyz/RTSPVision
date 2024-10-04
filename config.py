import os
from dotenv import load_dotenv

load_dotenv()

IP = os.getenv("IP") or ""
PORT = os.getenv("PORT") or ""
USERNAME = os.getenv("USERNAME") or ""
PASSWORD = os.getenv("PASSWORD") or ""
RTSP_URL = os.getenv("RTSP_URL") or ""

IS_DEBUG = os.getenv("IS_DEBUG") or False

