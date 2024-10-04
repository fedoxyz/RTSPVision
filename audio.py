import pyaudio
import threading
import subprocess
import queue
import json
from logger import logger

def get_stream_info(url):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    audio_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'audio'), None)
    return audio_stream

def read_audio(process, audio_queue):
    while True:
        in_bytes = process.stdout.read(4096)
        if not in_bytes:
            break
        audio_queue.put(in_bytes)

def play_audio(audio_queue, stream):
    while True:
        audio_data = audio_queue.get()
        if audio_data is None:
            break
        stream.write(audio_data)


def start_audio(url):
    audio_stream = get_stream_info(url)
    if audio_stream is None:
        logger.warning("No audio stream found.")
        return

    # Audio capture using ffmpeg
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', url,
        '-vn',  # Disable video
        '-acodec', 'pcm_s16le',
        '-ar', '44100',
        '-ac', '2',
        '-f', 's16le',
        'pipe:1'
    ]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    output=True)

    audio_queue = queue.Queue()
    audio_thread = threading.Thread(target=read_audio, args=(process, audio_queue))
    audio_thread.start()

    play_thread = threading.Thread(target=play_audio, args=(audio_queue, stream))
    play_thread.start()

    logger.info("Audio started streaming")

