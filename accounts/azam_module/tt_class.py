import requests
import os
import uuid
import json
from dotenv import load_dotenv


class AzureTranslator:
    """
    A class to interact with the Azure Translator Text API.

    Attributes:
    - key (str): The Azure API key.
    - endpoint (str): The Azure API endpoint.
    - location (str): The Azure region/location.
    """

    def __init__(self):
        """
        Initialize the Azure Translator Text API client.
        """
        load_dotenv()
        self.key = os.getenv('az-key')
        self.endpoint = os.getenv('az-endpoint')
        self.location = os.getenv('az-location')

    def translate_text(self, source_text, source_language, target_languages):
        """
        Translate text using the Azure Translator Text API.

        Args:
        - source_text (list): list of text to be translated.
        - target_languages (list): A list of target languages (e.g., ['ur', 'ar']).

        Returns:
        - dict: The translated text.
        """
        path = '/translate'
        constructed_url = self.endpoint + path

        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': target_languages
        }

        headers = {
            'Ocp-Apim-Subscription-Key': self.key,
            'Ocp-Apim-Subscription-Region': self.location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        body = [{'text': text} for text in source_text]

        request = requests.post(
            constructed_url, params=params, headers=headers, json=body)
        response = request.json()

        result = json.dumps(response, sort_keys=True,
                            ensure_ascii=False, indent=4, separators=(',', ': '))

        result = json.loads(result)

        return result


if __name__ == '__main__':
    # Example usage:
    translator = AzureTranslator()
    source_text = [
        'I would really like to drive your car around the block a few times!',
        'When will you come back?'
    ]
    source_language = 'en'
    target_languages = ['ur']
    tuple_list = translator.translate_text(
        source_text, source_language, target_languages)
    print('Tuple List: ', tuple_list)

    text_values = [translation['text']
                   for d in tuple_list for translation in d['translations']]
    # Join all 'text' values
    joined_text = ' '.join(text_values)

    print(f"joined = {joined_text}")
    '''
    Output: 
    Trans Text:  میں واقعی آپ کی گاڑی کو بلاک کے ارد گرد چند بار چلانا چاہتا ہوں!
    Tuple List:  [('میں واقعی آپ کی گاڑی کو بلاک کے ارد گرد چند بار چلانا چاہتا ہوں!', 'ur')]
    '''
