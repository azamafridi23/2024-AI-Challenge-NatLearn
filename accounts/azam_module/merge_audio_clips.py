import os
from pydub import AudioSegment


def merge(tuple_list, path_of_folder_to_merge, original_audio_path, name_of_merged_audio_wav):
    timestamps = [(data[1], data[2]) for data in tuple_list]
    original_audio = AudioSegment.from_file(original_audio_path)
    total_len_of_audio_should_be = len(original_audio) / 1000  # in s

    final_audio = None
    if len(timestamps) == 0:
        return 'timestamps length is zero'

    diff = timestamps[0][0]
    if (diff > 0):
        empty_audio = AudioSegment.silent(duration=diff*1000)
        final_audio = empty_audio

    for index, tup in enumerate(timestamps):
        tts_file_name = os.path.join(
            path_of_folder_to_merge, f'sync_audio_{index}.wav')
        audio = AudioSegment.from_file(tts_file_name)
        if final_audio is None:
            final_audio = audio
        else:
            final_audio += audio

        if index != len(timestamps)-1:
            diff = timestamps[index+1][0]-tup[1]
            if diff != 0:
                empty_audio = AudioSegment.silent(duration=diff*1000)
                final_audio += empty_audio

    if timestamps[len(timestamps)-1][1] != total_len_of_audio_should_be:
        empty_audio = AudioSegment.silent(duration=diff*1000)
        final_audio += empty_audio

    final_audio.export(name_of_merged_audio_wav, format="wav")

    return 'completed'


if __name__ == '__main__':
    a = [(' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.', 2.193, 25.486),
         (" Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.", 25.486, 48.609)]

    merge(a, 'audios to merge', 'eng_audio.mp3')
