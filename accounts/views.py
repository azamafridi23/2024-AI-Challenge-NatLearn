import os
import sys
sys.path.append(
    "accounts/azam_module")
import MEGA_PIPELINE_VT
import MEGA_PIPELINE_CHATBOT
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Video, Translation
from .forms import CustomUserCreationForm, VideoForm, TranslationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout



def user_register(request):
    '''
        This view is responsible for user registration
    '''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # You can change 'login' to the desired URL name for login
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    '''
    This view is responsible for showing home page
    '''
    return render(request, 'home.html')


def user_login(request):
    '''
    This view is responsible for handling user login requests
    '''
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # You can change 'home' to the desired URL name for the logged-in user's home page
            return redirect('dashboard')
    return render(request, 'login.html')

def user_logout(request):
    '''
    This view is responsible for user log out
    '''
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    '''
    This view is responsible for displaying dashboard to the user
    '''
    return render(request, 'dashboard.html')




class CombinedView(LoginRequiredMixin, View):
    '''
    This view is responsible for handling request for both video translation and chatbot interaction.
    '''
    template_name = 'combined.html' 

    def __init__(self, **kwargs):
        '''
        We initialize our LLM, embedding model, vector database and chatbot componenets
        '''
        super().__init__(**kwargs)
        self.llm, self.embedding_model, self.loader, self.docs, self.db, self.retriever, self.prompt, self.rag_chain_with_source = MEGA_PIPELINE_CHATBOT.chatbot_init('docs_for_chatbot')
        self.chat_history = []

    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(user=request.user)
        translations = Translation.objects.filter(user=request.user)
        form = VideoForm()
        return render(request, self.template_name, {'form': form, 'videos': videos, 'translations': translations})

    def post(self, request, *args, **kwargs):
        try:
            print("Request:", request.POST)
            if 'query' in request.POST: #  Check if the request is for chatbot
                query = request.POST.get('query', '')
                chat_history = request.POST.getlist('chat_history[]', [])
                response, updated_chat_history = MEGA_PIPELINE_CHATBOT.gen_answer(query, self.rag_chain_with_source, chat_history)
                response_data = {
                    'chat_history': updated_chat_history,
                    'response': response,
                }
                return JsonResponse(response_data)
            else: #  the request is for video translation
                form = VideoForm(request.POST, request.FILES)
                if form.is_valid():
                    video_file = request.FILES['uv']  # Assuming 'video_file' is the name of your file field
                    if not (video_file.name.endswith('.mp4') or video_file.name.endswith('.mp3')):
                        messages.error(request, 'Invalid file type. Please upload a .mp4 or .mp3 file.')
                        print("Invalid file type. Please upload a .mp4 or .mp3 file.")
                        return redirect('combined_view')
                    video = form.save(commit=False)
                    video.user = request.user
                    video.save()
                    if os.path.exists(video.uv.path):
                        print('XXXXXXXXXXX: VIDEO EXISTS')
                    else:
                        print("XXXXXXXXXXX: VIDEO DOESNOT EXIT!!!!")

                    MEGA_PIPELINE_VT.pipeline(input_video_path=video.uv.path, source_lang=video.source_lang,
                                            target_lang=video.target_lang,voice_type=int(video.voice_type))

                    translation = Translation()
                    translation.user = request.user
                    translation.title = video.title
                    filename = os.path.basename(video.uv.path)
                    new_path = os.path.join('translated_videos', filename)
                    print(f'filename: {filename} \n new_path: {new_path}')
                    current_directory = os.getcwd()
                    files_and_directories = os.listdir(current_directory)
                    print("Current Directory:", current_directory)
                    print("Files and Directories:", files_and_directories)

                    with open('TEMP_FOLDER_FOR_TRANSLATION/TRANSLATED_VIDEO.mp4', 'rb') as f:
                        translation.tv.save(new_path, ContentFile(f.read()))
                    translation.save()

                    MEGA_PIPELINE_VT.delete_folder()
                    return redirect('combined_view')
                else:
                    videos = Video.objects.filter(user=request.user)
                    translations = Translation.objects.filter(user=request.user)
                    return render(request, self.template_name, {'form': form, 'videos': videos, 'translations': translations})
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred: {e}")
            return HttpResponse("An error occurred while processing your request. Please try again later.", status=500)
            