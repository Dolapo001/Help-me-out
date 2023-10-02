import os
import speech_recognition as sr

from moviepy.editor import VideoFileClip
from celery import shared_task
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from api.models import Video, Transcription


@shared_task
def transcribe_video(video_id):
    try:
        video = Video.objects.get(pk=video_id)
    except Video.DoesNotExist:
        return

    temp_audio_path = 'temp_audio.wav'

    video_clip = VideoFileClip(video.video_data.path)
    video_duration = video_clip.duration
    video_clip.close()

    extraction_duration = min(60, video_duration)

    ffmpeg_extract_subclip(video.video_data.path, 0, extraction_duration, targetname=temp_audio_path)

    recognizer = sr.Recognizer()

    with sr.AudioFile(temp_audio_path) as source:
        audio_text = recognizer.recognize_google(source)

    transcription = Transcription(video=video, text=audio_text)
    transcription.save()

    os.remove(temp_audio_path)

    return transcription.text
