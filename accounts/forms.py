from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Video, Translation


class CustomUserCreationForm(UserCreationForm):
    '''
    This form is used for user registration
    '''
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'password1', 'password2']

class VideoForm(forms.ModelForm):
    '''
    This form is used when user is uploading videos for translation
    '''
    class Meta:
        model = Video
        fields = ['title', 'uv','source_lang','target_lang','voice_type'  ] #ed by azam

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['title', 'tv'] 

