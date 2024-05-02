from moviepy.editor import VideoFileClip, AudioFileClip


def add_audio(input_video_path, new_audio_path, output_video_path):
    '''
    This function is used to add new audio to a video
    '''
    # Load the video clip
    video_clip = VideoFileClip(input_video_path)

    # Remove the original audio from the video
    video_clip = video_clip.set_audio(None)

    # Load the new audio clip
    new_audio_clip = AudioFileClip(new_audio_path)

    # Overlay the new audio clip onto the video clip
    video_clip = video_clip.set_audio(new_audio_clip)

    print(f'output_path = {output_video_path}')
    # Write the modified video clip to a file
    video_clip.write_videofile(
        output_video_path, codec="libx264", audio_codec="aac")


if __name__ == '__main__':
    # Example usage:
    input_video_path = "INPUT_VIDEO.mp4"
    new_audio_path = "C:\\Users\\Azam\Desktop\\3 FEB TESTING WORK\\TEMP_FOLDER_FOR_TRANSLATION\\stt_audios\\merged_audio.wav"
    output_video_path = "output_video.mp4"

    add_audio(input_video_path, new_audio_path, output_video_path)
