import subprocess


def convert_video_to_audio(input_file, output_file):
    '''
    This function is used to convert video to audio
    '''
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", "192k",
        "-ar", "44100",
        "-y",
        output_file
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(
            f"Successfully converted to audio and stored at {output_file}")

    except subprocess.CalledProcessError as e:
        print("Conversion Failed")


if __name__ == '__main__':
    # Usage example:
    convert_video_to_audio("output_trimmed.mp4", "eng_audio.wav")
