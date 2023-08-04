from pytube import YouTube
import whisper
from transformers import pipeline
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates


def download_and_summarize_youtube_video(youtube_video_url, max_length=100):
    # Create a YouTube object
    yt = YouTube(youtube_video_url)

    # Get the video title and thumbnail URL
    video_title = yt.title
    video_title_cleaned = video_title.replace(" ", "") + ".mp3"
    thumbnail_url = yt.thumbnail_url

    # Get the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    if audio_stream is not None:
        # Download the audio to the specified output path (folder "audio" in this case)
        output_path = "audio"
        audio_stream.download(output_path=output_path, filename=video_title_cleaned)
        print("Audio downloaded successfully!")

        # Access the downloaded audio file and read its content into a variable
        audio_file_path = f"{output_path}/{video_title_cleaned}"
        with open(audio_file_path, "rb") as file:
            audio_data = file.read()

        # Transcribe the audio to text using Whisper
        model = whisper.load_model("base")
        result = model.transcribe("/content/audio/"+video_title_cleaned)
        transcript = result["text"]
        print(transcript)

        # Summarize the transcript using Hugging Face's pipeline
        summarizer = pipeline('summarization')
        summary = summarizer(transcript, max_length=max_length, min_length=30, do_sample=False)
        video_summary = summary[0]['summary_text']

        return video_title, video_summary, thumbnail_url

    else:
        print("No audio stream found for download.")
        return None, None, None

# Example usage
youtube_video_url = "https://www.youtube.com/watch?v=N6GyU9PHyQo"
max_length = 100
video_title, video_summary, thumbnail_url = download_and_summarize_youtube_video(youtube_video_url, max_length)
print("Video Title:", video_title)
print("Video Summary:", video_summary)
print("Thumbnail URL:", thumbnail_url)