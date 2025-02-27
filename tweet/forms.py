from django import forms
from .models import tweet
from .models import photo
from .models import premium_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class tweetforms(forms.ModelForm):
  class Meta:
    model=tweet
    fields=['Text','photo']
class UserRegistration(UserCreationForm):
  email=forms.EmailField(required=True)
  class Meta:
    model=User
    fields=('username','email','password1','password2')
class photo_form(forms.ModelForm):
  class Meta:
    model=photo
    fields=['user_photo']

class pu_form(forms.ModelForm):
  class Meta:
    model=premium_user
    fields=['is_premium']
class ChatbotForm(forms.Form):
    message = forms.CharField(label="Your Message", widget=forms.TextInput(attrs={"class": "form-control"}))