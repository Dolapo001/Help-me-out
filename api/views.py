from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Video, VideoChunk, Transcription
from .serializers import VideoSerializer, TranscriptionSerializer
from .tasks import transcribe_video
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, HttpResponse
from moviepy.editor import VideoFileClip
from api.utils import encode_video


class CreateView(APIView):
    @staticmethod
    def post(request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.save()
            chunked_upload = VideoChunk(video=video)
            chunked_upload.save()
            return Response({"detail": "Video created. You can now start uploading"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppendVideoView(APIView):
    def post(self, request, video_id, format=None):
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        video_data = request.data.get('video_data', b'')

        if video_data:
            video_chunk = VideoChunk(video=video, chunk_data=video_data)
            video_chunk.save()

            if video_chunk.is_completed():
                video.status = 'completed'
                video.save()

                encoded_video_path = self.encode_video(video)

                transcribe_video.delay(video_id)

                return Response({"detail": "Video data appended successfully.", "encoded_video_path": encoded_video_path}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Video data received successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No video data received."}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def encode_video(video):
        video_data = b''.join(chunk.chunk_data for chunk in VideoChunk.objects.filter(video=video))
        encoded_video_path = 'media/encoded_videos/video_{video.id}.mp4'

        encode_video(video_data, encoded_video_path)

        video_data = b''.join(chunk.chunk_data for chunk in VideoChunk.objects.filter(video=video))
        video_clip = VideoFileClip(video_data)
        video_clip.write_videofile(encoded_video_path, codec='libx264')

        return encoded_video_path


class GetVideoView(APIView):
    @staticmethod
    def get(request, video_id, format=None):
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        if video.status != 'completed':
            return Response({"detail": "Video not yet completed."}, status=status.HTTP_400_BAD_REQUEST)

        video_url = request.build_absolute_uri(reverse('video-file', args=[video_id]))

        serializer = VideoSerializer(video)
        transcriptions = Transcription.objects.filter(video=video)
        transcription_serializer = TranscriptionSerializer(transcriptions, many=True)
        serialized_transcriptions = transcription_serializer.data

        response_data = {
            "video": serializer.data,
            "transcriptions": serialized_transcriptions,
            "video_url": video_url
        }

        return Response(response_data, status=status.HTTP_200_OK)


class CompleteVideoView(APIView):
    @staticmethod
    def post(request, video_id, format=None):
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        if video.status != 'completed':
            video.status = 'completed'
            video.save()
            transcribe_video.delay(video_id)

        video_url = request.build_absolute_uri(reverse('video-detail', args=[video_id]))

        return Response({
            "detail": "Video marked as complete. Transcription process initiated.",
            "video_url": video_url
        }, status=status.HTTP_200_OK)


class VideoFileView(APIView):
    @staticmethod
    def get(request, video_id):
        try:
            video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist:
            return Response({"detail": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        if video.status != 'completed':
            return Response({"detail": "Video not yet completed."}, status=status.HTTP_400_BAD_REQUEST)

        video_file = open(video.video_file.path, 'rb')
        response = HttpResponse(video_file, content_type='video/mp4')
        response['Content-Disposition'] = f'inline; filename="{video.file_name}"'

        return response
