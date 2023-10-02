from chunked_upload.models import ChunkedUpload
from django.db import models

# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('recording', 'Recording'), ('completed', 'Completed')],
        default='recording'
    )

    video_data = models.FileField(upload_to='videos/', null=True, blank=True)

    def __str__(self):
        return self.title


class Transcription(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Transcription for {self.video.title}"


class VideoChunk(ChunkedUpload):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    @property
    def is_completed(self):
        # Check if the chunked upload is complete.
        return self.status == 'uploaded'
