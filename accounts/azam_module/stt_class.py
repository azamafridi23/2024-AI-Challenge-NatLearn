import whisperx
import gc


class WhisperTranscriber:
    """
    A class to convert speech to text and provide wordlevel timestamps

    Attributes:
    - device (str): The device to use for processing (e.g., "cuda").
    - audio_file (str): The path to the input audio file.
    - batch_size (int): The batch size for transcribing.
    - compute_type (str): The compute type for processing (e.g., "float16").
    - model_dir (str): The directory to save/load the model from.
    - model (whisperx.WhisperXModel): The loaded model for transcribing.
    """

    def __init__(self, model_dir="whisper_original_model_path/", device="cuda",
                 batch_size=16, compute_type="float16"):
        self.device = device
        self.batch_size = batch_size
        self.compute_type = compute_type
        self.model_dir = model_dir
        self.model = self.load_model()

    def load_model(self):
        """
        Load the whisper model.

        Returns:
        - whisperx.WhisperXModel: The loaded whisper model.
        """
        print("hi")
        return whisperx.load_model("large", self.device, compute_type=self.compute_type, download_root=self.model_dir)

    def transcribe(self, audio_file):
        """
        Transcribe the audio file using the loaded model.

        sample input: audio_file="whisperx/whisperx output files/input.wav"

        Returns:
        - dict: The transcribed segments.
        """
        audio = whisperx.load_audio(audio_file)
        result = self.model.transcribe(audio, batch_size=self.batch_size)
        trans_text = result["segments"]

        return trans_text

    def transcribe_and_align_segments(self, audio_file, language=None):
        '''
        returns transcribed_text, tuple_list, aligned_text

        transcribed_text: the transcribed text
        tuple_list: list of tuples of (text, start, end)
        aligned_text: aligned text        
        '''
        audio = whisperx.load_audio(audio_file)

        # Transcribe Text
        if language is not None:
            result = self.model.transcribe(
                audio, batch_size=self.batch_size, language=language)
            print("language is provided-printed by azam")
        else:
            result = self.model.transcribe(audio, batch_size=self.batch_size)

        data = result["segments"]

        transcribed_text = ' '.join(item['text'] for item in data)
        tuple_list = [(item['text'], item['start'], item['end'])
                      for item in data]

        # Align Text
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"], device=self.device)
        result2 = whisperx.align(result["segments"], model_a,
                                 metadata, audio, self.device, return_char_alignments=False)
        aligned_text = result2["segments"]

        return transcribed_text, tuple_list, aligned_text


if __name__ == '__main__':
    # Example usage:
    transcriber = WhisperTranscriber()
    # trans_text, tuple_list, alig_text = transcriber.transcribe_and_align_segments(
    #     audio_file=r"C:\Users\azam\Desktop\Deployed Natlearn\XWHISPERX WITH DJANGO TRY\Azam Final Work Temp\app\TEMP_FOLDER_FOR_TRANSLATION\original_audio.wav",language='en')

    # print('#'*50)
    # print('transcribed_text = ', trans_text)
    # print('tuple_list = ', tuple_list)
    # print('aligned_text = ', alig_text)


'''

transcribed_text =   Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.  Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.
-----------------------------------
tuple_list =  [(' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth. He even vastly exaggerated the size and the value of his own apartment in New York.', 2.193, 25.486), (" Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation. If found guilty, it could be facing a $250 million fine. And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing. OK, Sarah, thank you for that. Sarah Smith reporting live for us.", 25.486, 48.609)]
--------------------------------
aligned_text =  [{'start': 2.233, 'end': 20.323, 'text': ' Well, a judge in a civil trial in New York has ruled that Donald Trump has lied about the value of his assets, inflating them to try and get cheaper loans, that he basically exaggerated his wealth by over $2 billion by lying about what his buildings, hotels, golf clubs were worth.', 'words': [{'word': 'Well,', 'start': 2.233, 'end': 2.413, 'score': 0.512}, {'word': 'a', 'start': 2.493, 'end': 2.513, 'score': 0.999}, {'word': 'judge', 'start': 2.593, 'end': 2.873, 'score': 0.955}, {'word': 'in', 'start': 2.933, 'end': 3.013, 'score': 0.827}, {'word': 'a', 'start': 3.033, 'end': 3.073, 'score': 0.563}, {'word': 'civil', 'start': 3.194, 'end': 3.494, 'score': 0.909}, {'word': 'trial', 'start': 3.534, 'end': 3.834, 'score': 0.785}, {'word': 'in', 'start': 3.874, 'end': 3.934, 'score': 0.755}, {'word': 'New', 'start': 3.954, 'end': 4.014, 'score': 0.531}, {'word': 'York', 'start': 4.074, 'end': 4.374, 'score': 0.794}, {'word': 'has', 'start': 4.414, 'end': 4.654, 'score': 0.912}, {'word': 'ruled', 'start': 4.714, 'end': 4.955, 'score': 0.81}, {'word': 'that', 'start': 4.975, 'end': 5.095, 'score': 0.916}, {'word': 'Donald', 'start': 5.155, 'end': 5.515, 'score': 0.85}, {'word': 'Trump', 'start': 5.575, 'end': 5.855, 'score': 0.852}, {'word': 'has', 'start': 5.955, 'end': 6.215, 'score': 0.722}, {'word': 'lied', 'start': 6.375, 'end': 6.756, 'score': 0.754}, {'word': 'about', 'start': 6.956, 'end': 7.176, 'score': 0.899}, {'word': 'the', 'start': 7.196, 'end': 7.276, 'score': 0.826}, {'word': 'value', 'start': 7.316, 'end': 7.656, 'score': 0.734}, {'word': 'of', 'start': 7.696, 'end': 7.756, 'score': 0.775}, {'word': 'his', 'start': 7.796, 'end': 7.936, 'score': 0.616}, {'word': 'assets,', 'start': 8.136, 'end': 8.517, 'score': 0.865}, {'word': 'inflating', 'start': 8.577, 'end': 9.117, 'score': 0.897}, {'word': 'them', 'start': 9.137, 'end': 9.257, 'score': 0.994}, {'word': 'to', 'start': 9.297, 'end': 9.377, 'score': 0.774}, {'word': 'try', 'start': 9.417, 'end': 9.577, 'score': 0.854}, {'word': 'and', 'start': 9.597, 'end': 9.677, 'score': 0.931}, {'word': 'get', 'start': 9.717, 'end': 9.837, 'score': 0.863}, {'word': 'cheaper', 'start': 10.177, 'end': 10.558, 'score': 0.867}, {'word': 'loans,', 'start': 10.618, 'end': 10.998, 'score': 0.777}, {'word': 'that', 'start': 11.038, 'end': 11.178, 'score': 0.808}, {'word': 'he', 'start': 11.238, 'end': 11.358, 'score': 0.837}, {'word': 'basically', 'start': 11.698, 'end': 12.199, 'score': 0.848}, {'word': 'exaggerated', 'start': 12.339, 'end': 13.219, 'score': 0.801}, {'word': 'his', 'start': 13.299, 'end': 13.459, 'score': 0.678}, {'word': 'wealth', 'start': 13.539, 'end': 13.86, 'score': 0.862}, {'word': 'by', 'start': 13.98, 'end': 14.12, 'score': 0.834}, {'word': 'over', 'start': 14.24, 'end': 14.42, 'score': 0.98}, {'word': '$2'}, {'word': 'billion', 'start': 14.88, 'end': 15.36, 'score': 0.792}, {'word': 'by', 'start': 15.881, 'end': 16.021, 'score': 0.716}, {'word': 'lying', 'start': 16.381, 'end': 16.701, 'score': 0.971}, {'word': 'about', 'start': 16.761, 'end': 16.981, 'score': 0.843}, {'word': 'what', 'start': 17.041, 'end': 17.161, 'score': 0.909}, {'word': 'his', 'start': 17.201, 'end': 17.321, 'score': 0.712}, {'word': 'buildings,', 'start': 17.421, 'end': 18.002, 'score': 0.806}, {'word': 'hotels,', 'start': 18.082, 'end': 18.762, 'score': 0.775}, {'word': 'golf', 'start': 18.902, 'end': 19.182, 'score': 0.882}, {'word': 'clubs', 'start': 19.223, 'end': 19.503, 'score': 0.878}, {'word': 'were', 'start': 19.583, 'end': 19.803, 'score': 0.695}, {'word': 'worth.', 'start': 20.083, 'end': 20.323, 'score': 0.869}]}, {'start': 20.363, 'end': 25.066, 'text': 'He even vastly exaggerated the size and the value of his own apartment in New York.', 'words': [{'word': 'He', 'start': 20.363, 'end': 20.463, 'score': 0.734}, {'word': 'even', 'start': 20.643, 'end': 20.863, 'score': 0.733}, {'word': 'vastly', 'start': 21.024, 'end': 21.444, 'score': 0.804}, {'word': 'exaggerated', 'start': 21.524, 'end': 22.204, 'score': 0.865}, {'word': 'the', 'start': 22.264, 'end': 22.344, 'score': 0.864}, {'word': 'size', 'start': 22.424, 'end': 22.805, 'score': 0.91}, {'word': 'and', 'start': 22.865, 'end': 22.925, 'score': 0.524}, {'word': 'the', 'start': 22.945, 'end': 23.025, 'score': 0.824}, {'word': 'value', 'start': 23.065, 'end': 23.365, 'score': 0.729}, {'word': 'of', 'start': 23.405, 'end': 23.465, 'score': 0.751}, {'word': 'his', 'start': 23.505, 'end': 23.605, 'score': 0.847}, {'word': 'own', 'start': 23.705, 'end': 23.825, 'score': 0.702}, {'word': 'apartment', 'start': 23.865, 'end': 24.385, 'score': 0.904}, {'word': 'in', 'start': 24.525, 'end': 24.606, 'score': 0.839}, {'word': 'New', 'start': 24.666, 'end': 24.826, 'score': 0.884}, {'word': 'York.', 'start': 24.866, 'end': 25.066, 'score': 0.865}]}, {'start': 25.826, 'end': 32.833, 'text': ' Now, this case will now go forward to a civil trial in New York next week over other charges of fraud relating to the Trump organisation.', 'words': [{'word': 'Now,', 'start': 25.826, 'end': 25.966, 'score': 0.953}, {'word': 'this', 'start': 26.027, 'end': 26.187, 'score': 0.969}, {'word': 'case', 'start': 26.267, 'end': 26.487, 'score': 0.8}, {'word': 'will', 'start': 26.507, 'end': 26.687, 'score': 0.806}, {'word': 'now', 'start': 26.727, 'end': 26.847, 'score': 0.817}, {'word': 'go', 'start': 26.887, 'end': 27.028, 'score': 0.655}, {'word': 'forward', 'start': 27.088, 'end': 27.368, 'score': 0.999}, {'word': 'to', 'start': 27.408, 'end': 27.528, 'score': 0.691}, {'word': 'a', 'start': 27.568, 'end': 27.588, 'score': 0.989}, {'word': 'civil', 'start': 27.668, 'end': 27.968, 'score': 0.874}, {'word': 'trial', 'start': 28.009, 'end': 28.269, 'score': 0.943}, {'word': 'in', 'start': 28.309, 'end': 28.369, 'score': 0.757}, {'word': 'New', 'start': 28.409, 'end': 28.509, 'score': 0.984}, {'word': 'York', 'start': 28.549, 'end': 28.789, 'score': 0.919}, {'word': 'next', 'start': 28.849, 'end': 29.05, 'score': 0.68}, {'word': 'week', 'start': 29.13, 'end': 29.35, 'score': 0.901}, {'word': 'over', 'start': 29.43, 'end': 29.59, 'score': 0.993}, {'word': 'other', 'start': 29.71, 'end': 29.89, 'score': 0.962}, {'word': 'charges', 'start': 29.93, 'end': 30.391, 'score': 0.851}, {'word': 'of', 'start': 30.551, 'end': 30.611, 'score': 0.988}, {'word': 'fraud', 'start': 30.691, 'end': 31.011, 'score': 0.785}, {'word': 'relating', 'start': 31.052, 'end': 31.452, 'score': 0.813}, {'word': 'to', 'start': 31.492, 'end': 31.592, 'score': 0.834}, {'word': 'the', 'start': 31.612, 'end': 31.672, 'score': 0.987}, {'word': 'Trump', 'start': 31.732, 'end': 31.972, 'score': 0.82}, {'word': 'organisation.', 'start': 32.133, 'end': 32.833, 'score': 0.866}]}, {'start': 32.953, 'end': 37.338, 'text': 'If found guilty, it could be facing a $250 million fine.', 'words': [{'word': 'If', 'start': 32.953, 'end': 33.034, 'score': 0.998}, {'word': 'found', 'start': 33.114, 'end': 33.314, 'score': 0.796}, {'word': 'guilty,', 'start': 33.374, 'end': 33.774, 'score': 0.888}, {'word': 'it', 'start': 34.235, 'end': 34.295, 'score': 0.912}, {'word': 'could', 'start': 34.315, 'end': 34.435, 'score': 0.886}, {'word': 'be', 'start': 34.455, 'end': 34.515, 'score': 0.759}, {'word': 'facing', 'start': 34.555, 'end': 34.855, 'score': 0.891}, {'word': 'a', 'start': 34.895, 'end': 35.556, 'score': 0.422}, {'word': '$250'}, {'word': 'million', 'start': 36.197, 'end': 36.637, 'score': 0.819}, {'word': 'fine.', 'start': 37.058, 'end': 37.338, 'score': 0.794}]}, {'start': 37.838, 'end': 44.685, 'text': "And this is quite separate from the criminal cases, the four different criminal cases that Donald Trump's also facing.", 'words': [{'word': 'And', 'start': 37.838, 'end': 37.918, 'score': 0.887}, {'word': 'this', 'start': 37.958, 'end': 38.119, 'score': 0.74}, {'word': 'is', 'start': 38.339, 'end': 38.459, 'score': 0.826}, {'word': 'quite', 'start': 38.639, 'end': 38.899, 'score': 0.795}, {'word': 'separate', 'start': 39.08, 'end': 39.58, 'score': 0.776}, {'word': 'from', 'start': 39.64, 'end': 39.8, 'score': 0.824}, {'word': 'the', 'start': 39.84, 'end': 39.9, 'score': 0.992}, {'word': 'criminal', 'start': 40.121, 'end': 40.621, 'score': 0.836}, {'word': 'cases,', 'start': 40.681, 'end': 41.061, 'score': 0.863}, {'word': 'the', 'start': 41.122, 'end': 41.222, 'score': 0.772}, {'word': 'four', 'start': 41.322, 'end': 41.602, 'score': 0.842}, {'word': 'different', 'start': 41.702, 'end': 42.042, 'score': 0.864}, {'word': 'criminal', 'start': 42.183, 'end': 42.543, 'score': 0.832}, {'word': 'cases', 'start': 42.563, 'end': 42.903, 'score': 0.806}, {'word': 'that', 'start': 43.144, 'end': 43.264, 'score': 0.82}, {'word': 'Donald', 'start': 43.284, 'end': 43.564, 'score': 0.579}, {'word': "Trump's", 'start': 43.584, 'end': 43.844, 'score': 0.637}, {'word': 'also', 'start': 44.044, 'end': 44.325, 'score': 0.883}, {'word': 'facing.', 'start': 44.365, 'end': 44.685, 'score': 0.902}]}, {'start': 45.806, 'end': 47.007, 'text': 'OK, Sarah, thank you for that.', 'words': [{'word': 'OK,', 'start': 45.806, 'end': 45.946, 'score': 0.4}, {'word': 'Sarah,', 'start': 46.086, 'end': 46.447, 'score': 0.616}, {'word': 'thank', 'start': 46.467, 'end': 46.627, 'score': 0.814}, {'word': 'you', 'start': 46.667, 'end': 46.747, 'score': 0.856}, {'word': 'for', 'start': 46.767, 'end': 46.867, 'score': 0.876}, {'word': 'that.', 'start': 46.887, 'end': 47.007, 'score': 0.833}]}, {'start': 47.047, 'end': 48.309, 'text': 'Sarah Smith reporting live for us.', 'words': [{'word': 'Sarah', 'start': 47.047, 'end': 47.268, 'score': 0.642}, {'word': 'Smith', 'start': 47.288, 'end': 47.488, 'score': 0.815}, {'word': 'reporting', 'start': 47.508, 'end': 47.928, 'score': 0.487}, {'word': 'live', 'start': 47.948, 'end': 48.088, 'score': 0.309}, {'word': 'for', 'start': 48.109, 'end': 48.249, 'score': 0.516}, {'word': 'us.', 'start': 48.269, 'end': 48.309, 'score': 0.09}]}]

'''
