
# Help-Me-Out

## Introduction

This is a Django Rest Framework (DRF) project designed to support a Chrome Extension for recording and transcribing videos. The project allows users to upload videos, transcribe them, and associate transcriptions with the respective videos. It also provides API endpoints for video uploading, transcription, and retrieval.

## Features

- **Video Uploading:** Users can upload video files using the provided API.
- **Transcription Integration:** The project integrates with a transcription service to automatically transcribe videos.
- **Transcription Storage:** Transcriptions are associated with videos and stored in the system.
- **Video Playback:** Users can retrieve and play uploaded videos along with their transcriptions.

## Technologies Used

- Django: Backend web framework
- Django Rest Framework (DRF): For building RESTful APIs
- Django Chunked Upload: For Uploading videos received in chunks
- Transcription Service (Celery and Rabbitmq): For video transcriptions
- Amazon S3: For media file storage
- Swagger UI: For API documentation
- Postman: For testing API endpoints

## Setup

1. Clone this repository to your local environment.

2. Install the project's dependencies:

   pip install -r requirements.txt
   

3. Configure your Django settings:
   - Set up your database configuration.
   - Configure the media file handling to use Amazon S3.

4. Run the Django development server:
   
   python manage.py runserver


5. Access the Swagger UI documentation to explore and test the available API endpoints:

   http://localhost:8000/swagger/schema/


## Usage

- **Video Upload:** Use the API endpoint `/api/upload/` to upload video files.
- **Video Transcription:** Use the API endpoint `/api/transcription/` to initiate video transcription.

## API Documentation

The complete API documentation, including endpoint details, request/response formats, and usage instructions, is available in the Swagger UI documentation.

[Link to Swagger UI Documentation](https://help-me-out-api.onrender.com/swagger/schema/)

