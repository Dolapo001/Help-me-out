from django.urls import path
from .views import CreateView, AppendVideoView, CompleteVideoView, GetVideoView, VideoFileView

urlpatterns = [
    path('videos/create/', CreateView.as_view(), name='create_video'),

    path('videos/append/<int:video_id>/', AppendVideoView.as_view(), name='append_video'),

    path('videos/complete/<int:video_id>/', CompleteVideoView.as_view(), name='complete_video'),

    path('videos/<int:video_id>/', GetVideoView.as_view(), name='get_video'),

    path('videos/file/<int:video_id>/', VideoFileView.as_view(), name='video-file'),
]
