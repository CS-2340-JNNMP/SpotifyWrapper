from google.cloud import translate_v2 as translate
from django.conf import settings

class TranslationService:
    def __init__(self):
        self.client = translate.Client()  # Create a translation client
        self.api_key = settings.GOOGLE_API_KEY  # Get API key from settings

    def translate_text(self, text, target_language):
        # Translate text to the target language
        result = self.client.translate(text, target_lang=target_language, key=self.api_key)
        return result['translatedText']
