
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Video, Translation, Feedback


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['name', 'email', 'password1', 'password2']

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'uv','source_lang','target_lang','voice_type'  ] #ed by azam

class TranslationForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['title', 'tv'] 


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['translation', 'feedback']

    def __init__(self, user, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['translation'].queryset = Translation.objects.filter(user=user)
        self.fields['translation'].empty_label = "Select Translation"
        self.fields['feedback'].widget.attrs.update({'class': 'form-control'})
