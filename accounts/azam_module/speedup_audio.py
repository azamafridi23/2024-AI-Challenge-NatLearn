import os
from pydub import AudioSegment


def speedup_audio_for_timestamps(tuple_list, folder_path):

    timestamps = [(data[1], data[2]) for data in tuple_list]
    print("timestamps = ", timestamps)
    # List all files in the folder
    files = os.listdir(folder_path)

    # Count the number of files
    num_files = len(files)

    for index in range(num_files):
        tts_file_name = os.path.join(folder_path, f'tts_{index}.wav')
        audio = AudioSegment.from_file(tts_file_name)
        duration_of_prod_audio = len(audio) / 1000
        req_duration = timestamps[index][1] - timestamps[index][0]
        print(
            f'tts_file_name = {tts_file_name}, duration = {duration_of_prod_audio}, req = {req_duration}')

        if duration_of_prod_audio > req_duration:
            speedup_factor = duration_of_prod_audio / req_duration
            sped_up_audio = audio.speedup(speedup_factor, 150, 25)
            sync_audio_name = os.path.join(
                folder_path, f"sync_audio_{index}.wav")
            sped_up_audio.export(sync_audio_name, format="wav")
        else:
            sync_audio_name = os.path.join(
                folder_path, f"sync_audio_{index}.wav")
            audio.export(sync_audio_name, format="wav")

    return 'completed'


if __name__ == '__main__':
    # Example usage:
    a = [(' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.', 2.193, 25.486),
         (" Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.", 25.486, 48.609)]

    folder_path = 'audio files'

    speedup_audio_for_timestamps(a, folder_path)
