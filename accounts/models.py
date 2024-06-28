from django.db import models
from django.contrib.auth.models import AbstractUser
import os


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.username = self.email
        super().save(*args, **kwargs)


Source_Lang_Choices = [('english', 'english'), ('chinese', 'chinese'), ('urdu', 'urdu'), ('german', 'german'), ('spanish', 'spanish'), ('russian', 'russian'), ('korean', 'korean'), ('french', 'french'), ('japanses', 'japanses'), ('portugese', 'portugese'), ('turkish', 'turkish'), ('polish', 'polish'), ('dutch', 'dutch'), ('arabic', 'arabic'), ('swedish', 'swedish'), ('italian', 'italian'), ('indoesian', 'indoesian'), ('hindi', 'hindi'), ('finnish', 'finnish'), ('ukrainian', 'ukrainian'), ('romanian', 'romanian'), ('danish', 'danish'), ('hungarian', 'hungarian'), ('tamil', 'tamil'), ('norwegian', 'norwegian'), ('thai', 'thai'), ('persian', 'persian'), ('serbian', 'serbian')]

Target_Lang_Choices = [('english', 'english'), ('chinese', 'chinese'), ('urdu', 'urdu'), ('german', 'german'), ('spanish', 'spanish'), ('russian', 'russian'), ('korean', 'korean'), ('french', 'french'), ('japanses', 'japanses'), ('portugese', 'portugese'), ('turkish', 'turkish'), ('polish', 'polish'), ('dutch', 'dutch'), ('arabic', 'arabic'), ('swedish', 'swedish'), ('italian', 'italian'), ('indoesian', 'indoesian'), ('hindi', 'hindi'), ('finnish', 'finnish'), ('ukrainian', 'ukrainian'), ('romanian', 'romanian'), ('danish', 'danish'), ('hungarian', 'hungarian'), ('tamil', 'tamil'), ('norwegian', 'norwegian'), ('thai', 'thai'), ('persian', 'persian'), ('serbian', 'serbian')]

Voice_Type_Choices = [('0', 'Male'), ('1', 'Female')]

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='ali@natlean.com' )
    title = models.CharField(max_length=100)
    uv = models.FileField(upload_to='uploaded_videos/')

    source_lang = models.CharField(max_length=30,choices=Source_Lang_Choices,default='english')
    target_lang = models.CharField(max_length=30, choices=Target_Lang_Choices,default='urdu')
    
    voice_type = models.CharField(max_length=30, choices=Voice_Type_Choices, default='1')

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = os.path.splitext(self.uv.name)[0]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
 

class Translation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    tv = models.FileField(upload_to='')


    def __str__(self):
        return self.title
    

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.name


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    response = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message
    

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"Feedback for {self.translation.title} by {self.user.username}"



