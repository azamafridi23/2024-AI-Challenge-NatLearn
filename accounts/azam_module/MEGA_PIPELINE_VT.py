# -*- coding: utf-8 -*-

'''

THIS PIPELINE HAS BEEN TESTED AND IT IS WORKING FINE.


'''


import os
import shutil
import json
from stt_class import WhisperTranscriber
from tt_class import AzureTranslator
from tts_class import TextToSpeech

from add_audio_to_video import add_audio
from speedup_audio import speedup_audio_for_timestamps
from merge_audio_clips import merge
from video_to_audio import convert_video_to_audio
from lang_mapping_dicts import dic_for_lang_mapping, tts_dict
from dotenv import load_dotenv

from accounts.azam_module.vqa import encode_image, vqa_data
load_dotenv()


def make_folder(path='TEMP_FOLDER_FOR_TRANSLATION'):
    '''
        Checks if a folder 'path' exists. If it doesn't then it creates it. 
    '''
    if not (os.path.exists(path)):

        current_directory = os.path.abspath(os.path.dirname(__file__))
        os.mkdir(path)
        print(f'CREATED FOLDER AT {current_directory} named: {path}')


def delete_folder(folder_path='TEMP_FOLDER_FOR_TRANSLATION'):
    try:
        # Delete the folder and all its contents recursively
        shutil.rmtree(folder_path)
        print(
            f"Folder '{folder_path}' and its contents have been successfully deleted.")
    except Exception as e:
        print(f"Error deleting folder '{folder_path}': {e}")


def unique_file_name(path):
    # Find filename for chatbot docs
    file_name_for_chatbot_docs = None
    i = 0
    while (True):
        if os.path.exists(f'{path}/Text{i}.txt'):
            i += 1
        else:
            file_name_for_chatbot_docs = f'{path}/Text{i}.txt'
            break
    return file_name_for_chatbot_docs


def pipe1(input_file, output_file):  # Video to audio
    convert_video_to_audio(input_file, output_file)


def pipe2(input_video_path, source_lang, target_lang, original_audio_path, original_text_path, translated_text_path, translated_audio_folder_path, aligned_text_path, folder_path_for_chatbot_data,voice_type):
    ''' 
        Video translator transformer

    '''

    text_path_for_chatbot = unique_file_name(folder_path_for_chatbot_data)

    source_stt = dic_for_lang_mapping[source_lang][0]
    source_tt = dic_for_lang_mapping[source_lang][1]
    target_tt = [(dic_for_lang_mapping[target_lang][1])]
    print('tt ,', target_tt)
    print('source_tt = ', source_stt)
    source_tts = dic_for_lang_mapping[source_lang][2]

    # voice_name_for_tts = 'ur-PK-AsadNeural'
    # change 1 to 0 for male voice
    voice_name_for_tts = tts_dict[(dic_for_lang_mapping[target_lang][2])][voice_type]

    # STT conversion
    try:
        transcriber = WhisperTranscriber()
        print(f'original_audio_path = {original_audio_path}')
        transcribed_text, tuple_list_of_stt, aligned_text = transcriber.transcribe_and_align_segments(
            audio_file=original_audio_path, language=source_stt)
        # writing stt transcribed text output to file
        with open(original_text_path, 'w',encoding='utf-8') as file:
            file.write(transcribed_text)
        # writing aligned text output to file
        with open(aligned_text_path, 'w',encoding='utf-8') as file:
            file.write(str(aligned_text))
        if (source_lang == 'english'):
            with open(text_path_for_chatbot, 'w') as file:
                file.write(transcribed_text)

    except Exception as e:
        print("STT FAILED DUE TO: ",e)
        return f'Speech to text failed due to : {e}', 0, 0, 0

    # tuple_list_of_stt = [(' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.', 2.193, 25.486), (
    #     " Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.", 25.486, 48.609)]

    # TT conversion
    try:
        translator = AzureTranslator()
        source_text = [text
                       for text, _, _ in tuple_list_of_stt]
        print('source_text = ', source_text)
        tt_json = translator.translate_text(
            source_text, source_tt, target_tt)
        print("tt_json = ", tt_json)
        print('kkk = ', tt_json[0]['translations'][0]['text'])
        if (target_lang == 'english'):
            text_values = [translation['text']
                           for d in tt_json for translation in d['translations']]
            # Join all 'text' values
            joined_text = '  '.join(text_values)
            with open(text_path_for_chatbot, 'w') as file:
                file.write(joined_text)


        tuple_list_of_tt = []
        for i in range(len(tt_json)):
            translated_text = tt_json[i]['translations'][0]['text']
            start_time = tuple_list_of_stt[i][1]
            end_time = tuple_list_of_stt[i][2]
            myt = (translated_text, start_time, end_time)
            tuple_list_of_tt.append(myt)

        if not(source_lang == 'english' or target_lang == 'english'):
            tt_json = translator.translate_text(source_text, source_tt, 'en')
            text_values = [translation['text']
                           for d in tt_json for translation in d['translations']]
            # Join all 'text' values
            joined_text = '  '.join(text_values)

            with open(text_path_for_chatbot, 'w') as file:
                file.write(joined_text)

    except Exception as e:
        print("TT FAILED DUE TO:", e)
        return f'Text translation failed due to : {e}', 0, 0, 0

    # TTS conversion
    try:
        tts = TextToSpeech()
        tuple_list_of_tts = []

        for index, tup in enumerate(tuple_list_of_tt):
            tts_file_name = os.path.join(
                translated_audio_folder_path, f'tts_{index}.wav')
            print(tts_file_name)
            tts.speech_synthesis(
                tup[0], output_file=tts_file_name, voice_name=voice_name_for_tts)
            start_time = tuple_list_of_stt[index][1]
            end_time = tuple_list_of_stt[index][2]
            myt = (tts_file_name, start_time, end_time)
            tuple_list_of_tts.append(myt)

    except Exception as e:
        print("TTS FAILED DUE TO:", e)
        return f'Text to speech failed due to : {e}', 0, 0, 0

    return 'completed', tuple_list_of_stt, tuple_list_of_tt, tuple_list_of_tts


# forced synchronization by speedingup
def pipe3(tuple_list, audios_folder_path):
    speedup_audio_for_timestamps(
        tuple_list, audios_folder_path)


def pipe4(tuple_list, path_of_folder_to_merge, original_audio_path, name_of_merged_audio_wav):  # merge audio clipss
    merge(tuple_list, path_of_folder_to_merge,
          original_audio_path, name_of_merged_audio_wav)


def pipe5(input_video_path, new_audio_path, output_video_path):
    add_audio(input_video_path, new_audio_path, output_video_path)


def pipeline(input_video_path, source_lang, target_lang, folder_path_for_chatbot_data='docs_for_chatbot', temp_folder_for_translation_path='TEMP_FOLDER_FOR_TRANSLATION',voice_type=1):

    # # # make temp folder for translation
    make_folder(temp_folder_for_translation_path)

    make_folder(folder_path_for_chatbot_data)

    original_audio_path = f'{temp_folder_for_translation_path}/original_audio.wav'
    print('PIPE1 STARTED')
    # # video to audio
    pipe1(input_video_path, original_audio_path)
    print('PIPE1 ENDED')

    original_text_path = f'{temp_folder_for_translation_path}/original_text.txt'
    translated_text_path = f'{temp_folder_for_translation_path}/translated_text.txt'
    aligned_text_path = f'{temp_folder_for_translation_path}/aligned_text.txt'

    translated_audio_folder_path = f'{temp_folder_for_translation_path}/translated_audios'

    name_of_merged_audio_wav = f'{temp_folder_for_translation_path}/merged_audio.wav'

    print('PIPE2 STARTED')
    print('path: ', translated_audio_folder_path)
    # to store stt produced audios
    make_folder(translated_audio_folder_path)
    # multilingual translation
    status, tuple_list_of_stt, tuple_list_of_tt, tuple_list_of_tts = pipe2(
        input_video_path, source_lang, target_lang, original_audio_path, original_text_path, translated_text_path, translated_audio_folder_path, aligned_text_path, folder_path_for_chatbot_data,voice_type)
    print('PIPE2 ENDED')

    # tuple_list_of_stt = [(' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.', 2.193, 25.486), (
    #     " Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.", 25.486, 48.609)]

    print('PIPE3 STARTED')
    # forced sync
    pipe3(tuple_list_of_stt, translated_audio_folder_path)
    print('PIPE3 ENDED')

    print('PIPE4 STARTED')
    # merge audio
    pipe4(tuple_list_of_stt, translated_audio_folder_path,
          original_audio_path, name_of_merged_audio_wav)
    print('PIPE4 ENDED')

    print(f'temp_folder_for_trans = {temp_folder_for_translation_path}')
    output_video_path = f'{temp_folder_for_translation_path}/TRANSLATED_VIDEO.mp4'
    print('PIPE5 STARTED')
    # add audio to video
    pipe5(input_video_path, name_of_merged_audio_wav, output_video_path)
    print('PIPE5 ENDED')
    print('PIPE6 STARTED(VISUALQ QA)')
    try:
        vqa_data(input_video_path, temp_folder_for_translation_path,folder_path_for_chatbot_data)
    except Exception as e:
        print(f'VQA FAILED DUE TO: {e}')
    print('PIPE6 ENDED(VISUALQ QA)')

    print("PIPELINE COMPLETED")


if __name__ == '__main__':
    input_video_path = 'output_trimmed.mp4'
    # output_video_path = 'FINAL_OUTPUT_VIDEO.mp4'
    source_lang = 'english'
    target_lang = 'urdu'
    # folder_path_for_chatbot = 'chatbot_docs'
    pipeline(input_video_path, source_lang,
             target_lang)
