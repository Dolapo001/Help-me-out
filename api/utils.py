from moviepy.editor import VideoFileClip


def encode_video(video_data, output_path, codec='libx264', audio_codec='aac', resolution=None, other_options=None):
    video_clip = VideoFileClip(video_data)

    codec_options = {"codec": codec, "audio_codec": audio_codec}

    if resolution:
        codec_options["resolution"] = resolution

    if other_options:
        codec_options.update(other_options)

    video_clip.write_videofile(output_path, codec=codec_options)

    return output_path
