import os
import random
import time
import subprocess

# Path to your local music files
MUSIC_DIR = './music_files'  # Replace this with your directory of music files
IMAGE_FILE = './static_image.png'  # Replace with your image file path (static image for video)

# Get list of audio files
AUDIO_FILES = [f for f in os.listdir(MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]

# Ensure the music directory exists
if not AUDIO_FILES:
    print("No music files found in the specified directory.")
    exit()

# Replace with your YouTube stream URL and stream key
stream_key = "m5dp-tt7s-e18e-gze0-3gge"  # Replace with your actual stream key
rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

# Function to stream audio with static image to YouTube via FFmpeg
def stream_audio():
    while True:
        # Randomly select an audio file from the list
        audio_file = random.choice(AUDIO_FILES)
        audio_path = os.path.join(MUSIC_DIR, audio_file)

        print(f"Selected audio file: {audio_file}")
        print(f"Audio path: {audio_path}")

        # FFmpeg command to stream audio with static image
        ffmpeg_command = [
            'ffmpeg', 
            '-re',  # Read input at native frame rate
            '-i', audio_path,  # Input audio file
            '-loop', '1',  # Loop the image
            '-i', IMAGE_FILE,  # Input static image
            '-c:v', 'libx264',  # Video codec
            '-preset', 'veryfast',  # Encoding preset
            '-c:a', 'aac',  # Audio codec
            '-b:a', '128k',  # Audio bitrate
            '-f', 'flv',  # Output format
            rtmp_url  # RTMP stream URL
        ]

        print(f"Executing FFmpeg command: {' '.join(ffmpeg_command)}")

        try:
            ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = ffmpeg_process.communicate()

            # Check for errors and log them
            if ffmpeg_process.returncode != 0:
                print(f"FFmpeg Error: {stderr.decode()}")
            else:
                print(f"Successfully started streaming: {audio_file}")
            print(f"FFmpeg Output: {stdout.decode()}")

        except Exception as e:
            print(f"Error while streaming audio file {audio_file}: {e}")

        time.sleep(5)  # Pause for 5 seconds before switching to the next track

# Start streaming
if __name__ == "__main__":
    print("Starting streaming process...")
    stream_audio()
