#!/bin/bash
# Define variables
RTSP_URL="123" 
LOG_FILE="rtsp_debug.log"

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg is not installed. Please install it before running the script."
    exit 1
fi

# Run ffmpeg with the RTSP URL and log options
echo "Starting ffmpeg to debug RTSP connection..."
ffmpeg -loglevel debug -rtsp_transport tcp -i "$RTSP_URL" -f null - 2> "$LOG_FILE"

# Print completion message
echo "Debugging completed. Check the log file: $LOG_FILE"

