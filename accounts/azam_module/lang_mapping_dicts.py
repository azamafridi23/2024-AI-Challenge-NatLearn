'''
These mappings are used for STT,TT, AND TTS MODELS
'''

dic_for_lang_mapping = {
    # tuple where first index val of the tuple is for STT MODEL, second index val is for TT MODEL and third index val is for TTS MODEL
    # stt: https://github.com/m-bain/whisperX/blob/e909f2f766b23b2000f2d95df41f9b844ac53e49/whisperx/tokenizer.py
    # tt: https://learn.microsoft.com/en-us/azure/ai-services/translator/language-support
    # tts: https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts

    'english': ('en', 'en', 'en-US'),
    'chinese': ('zh', 'zh-Hans', 'wuu-CN'),
    'urdu': ('ur', 'ur', 'ur-PK'),
    'german': ('de', 'de', 'de-DE'),
    'spanish': ('es', 'es', 'es-ES'),
    'russian': ('ru', 'ru', 'ru-RU'),
    'korean': ('ko', 'ko', 'ko-KR'),
    'french': ('fr', 'fr', 'fr-FR'),
    'japanses': ('ja', 'ja', 'ja-JP'),
    'portugese': ('pt', 'pt', 'pt-BR'),
    'turkish': ('tr', 'tr', 'tr-TR'),
    'polish': ('pl', 'pl', 'pl-PL'),
    'dutch': ('nl', 'nl', 'nl-NL'),
    'arabic': ('ar', 'ar', 'ar-EG'),  # Egyption arabic
    'swedish': ('sv', 'sv', 'sv-SE'),
    'italian': ('it', 'it', 'it-IT'),
    'indoesian': ('id', 'id', 'id-ID'),
    'hindi': ('hi', 'hi', 'hi-IN'),
    'finnish': ('fi', 'fi', 'fi-FI'),
    'ukrainian': ('uk', 'uk', 'uk-UA'),
    'romanian': ('ro', 'ro', 'ro-RO'),
    'danish': ('da', 'da'),
    'hungarian': ('hu', 'hu', 'hu-HU'),
    'tamil': ('ta', 'ta', 'ta-IN'),
    'norwegian': ('no', 'nb', 'nb-NO'),
    'thai': ('th', 'th', 'th-TH'),
    'persian': ('fa', 'fa', 'fa-IR'),
    'serbian': ('sr', '	sr-Latn', 'sr-LATN-RS')
}

tts_dict = {
    'en-US': ('en-US-AndrewNeural', 'en-US-AvaNeural'),  # MALE, FEMALE
    'wuu-CN': ('wuu-CN-YunzheNeural', 'wuu-CN-XiaotongNeural'),
    'ur-PK': ('ur-PK-AsadNeural', 'ur-PK-UzmaNeural'),
    'de-DE': ('de-DE-ConradNeural', 'de-DE-KatjaNeural'),
    'es-ES': ('es-ES-AlvaroNeural', 'es-ES-ElviraNeural'),
    'ru-RU': ('ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural'),
    'ko-KR': ('ko-KR-InJoonNeural', 'ko-KR-SunHiNeural'),
    'fr-FR': ('fr-FR-HenriNeural', 'fr-FR-DeniseNeural'),
    'ja-JP': ('ja-JP-KeitaNeural', 'ja-JP-NanamiNeural'),
    'pt-BR': ('pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural'),
    'tr-TR': ('tr-TR-AhmetNeural', 'tr-TR-EmelNeural'),
    'pl-PL': ('pl-PL-MarekNeural', 'pl-PL-AgnieszkaNeural'),
    'nl-NL': ('nl-NL-MaartenNeural', 'nl-NL-FennaNeural'),
    'ar-EG': ('ar-EG-ShakirNeural', 'ar-EG-SalmaNeural'),
    'sv-SE': ('sv-SE-MattiasNeural', 'sv-SE-SofieNeural'),
    'it-IT': ('it-IT-DiegoNeural', 'it-IT-IsabellaNeural'),
    'id-ID': ('id-ID-ArdiNeural', 'id-ID-GadisNeural'),
    'hi-IN': ('hi-IN-MadhurNeural', 'hi-IN-SwaraNeural'),
    'fi-FI': ('fi-FI-HarriNeural', 'fi-FI-SelmaNeural'),
    'uk-UA': ('uk-UA-OstapNeural', 'uk-UA-PolinaNeural'),
    'ro-RO': ('ro-RO-EmilNeural', 'ro-RO-AlinaNeural'),
    'da-DK': ('da-DK-JeppeNeural', 'da-DK-ChristelNeural'),
    'hu-HU': ('hu-HU-TamasNeural', 'hu-HU-NoemiNeural'),
    'ta-IN': ('ta-IN-ValluvarNeural', 'ta-IN-PallaviNeural'),
    'nb-NO': ('nb-NO-FinnNeural', 'nb-NO-PernilleNeural'),
    'th-TH': ('th-TH-NiwatNeural', 'th-TH-PremwadeeNeural'),
    'fa-IR': ('fa-IR-FaridNeural', 'fa-IR-DilaraNeural'),
    'sr-LATN-RS': ('sr-Latn-RS-NicholasNeural', 'sr-Latn-RS-SophieNeural')
}

if __name__=='__main__':
    print(len(dic_for_lang_mapping))
    a = [(i,i) for i in dic_for_lang_mapping.keys()]
    print(a)