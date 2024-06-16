import os
import json
from pytube import YouTube
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    UrlSource,
)
import httpx

class YouTubeScraper:
    def __init__(self, output_path="videos"):
        self.output_path = output_path

        # Create output directory if it doesn't exist
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # Initialize Deepgram client
        self.deepgram = self._initialize_deepgram()

    def _initialize_deepgram(self):
        try:
            deepgram_api_key = os.getenv("DEEPGRAM_API_KEY")
            if not deepgram_api_key:
                raise ValueError("DEEPGRAM_API_KEY environment variable is not set.")
            
            os.environ["DEEPGRAM_API_KEY"] = deepgram_api_key
            config = DeepgramClientOptions()
            return DeepgramClient("", config)
        except Exception as e:
            print(f"Error initializing Deepgram client: {e}")
            return None

    def scrape_video(self, video_url):
        try:
            print("Downloading YouTube video...")
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()
            video_path = os.path.join(self.output_path, f"{yt.title}.mp4")
            video.download(output_path=self.output_path, filename=yt.title)
            print(f"Video downloaded successfully: {video_path}")
            return video_path
        except Exception as e:
            print(f"An error occurred while downloading video: {e}")
            return None

    def get_transcription(self, video_url, save = False):
        try:
            print("Transcribing video to text...")
            payload = UrlSource(url=video_url)

            options = PrerecordedOptions(model="nova", smart_format=True)

            response = self.deepgram.listen.prerecorded.v("1").transcribe_file(
                payload, options, timeout=httpx.Timeout(300.0, connect=10.0)
            )

            response = response.to_json(indent=4)
            data = json.loads(response)
            transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]

            print("Transcription completed.")  

            if save:
                transcript_file = os.path.join(self.output_path, "transcript.txt")
                with open(transcript_file, "w") as f:
                    f.write(transcript)
                print(f"Transcript saved to: {transcript_file}")

            return transcript
        
        except Exception as e:
            print(f"An error occurred during transcription: {e}")
            return None
