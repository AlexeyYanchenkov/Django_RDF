import re
from rest_framework.exceptions import ValidationError

def validate_youtube_url(value):
    if 'youtube.com' not in value and 'youtu.be' not in value:
        raise ValidationError("Допустимы только ссылки на youtube.com или youtu.be")