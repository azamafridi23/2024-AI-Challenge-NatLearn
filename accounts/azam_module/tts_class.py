import os
import json
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk


class TextToSpeech:
    def __init__(self):
        '''
            Args:
            speech_key (str): Azure Speech service key.
            service_region (str): Azure Speech service region.
        '''
        load_dotenv()
        speech_key, service_region = os.getenv(
            'SPEECH_KEY'), os.getenv('SPEECH_REGION')
        self.speech_key = speech_key
        self.service_region = service_region
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.service_region)

    def speech_synthesis(self, text, output_file="AZURE_PROD_SPEECH2.wav", voice_name='ur-PK-AsadNeural'):
        '''
            Synthesizes speech from text and saves it to an audio file.

            Args:
                text (str): Text to be synthesized into speech.
                output_file (str): Path to save the synthesized audio file.
                voice_name (str): Name of the voice to be used for synthesis.
        '''

        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=output_file)

        # The language of the voice that speaks.
        self.speech_config.speech_synthesis_voice_name = voice_name

        speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config)

        speech_synthesis_result = speech_synthesizer.speak_text_async(
            text).get()

        if speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Issue in Azure text to speech: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print("Issue in Azure text to speech: {}".format(
                        cancellation_details.error_details))
                    print(
                        "Ensure that the speech resource key and region values are set")


if __name__ == '__main__':
    tts = TextToSpeech()
    text = "رفتار اور رفتار میں کیا فرق ہے؟ رفتار وہ وقت کی شرح ہے جس پر کوئی شے کسی راستے پر چل رہی ہوتی ہے ، جبکہ رفتار کسی شے کی حرکت کی شرح اور سمت ہے۔ "
    tts.speech_synthesis(text)
