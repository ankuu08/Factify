from django.shortcuts import render
from .models import tweet,photo,premium_user
from .forms import tweetforms,UserRegistration,photo_form,pu_form,ChatbotForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.models import User
import razorpay
from django.conf import settings
import google.generativeai as genai
from django.http import JsonResponse
# Create your views here.
# def tweet(request):
#   return render(request,'tweet/index1.html')

def tweet_list(request):
  if request.user.is_authenticated:
    tweets=tweet.objects.all().exclude(user=request.user).order_by('-created_at')
  else:
    tweets=tweet.objects.all().order_by('-created_at').distinct();
  pu = premium_user.objects.all()
  context = {
        'tweets': tweets,
        'pu':pu,
      # Adding another field
    }
  return render(request,'tweet/tweetlist.html',context)
@login_required
def create(request):
  if request.method=='POST':
    form=tweetforms(request.POST,request.FILES)
    if form.is_valid():
      tweets=form.save(commit=False)
      tweets.user=request.user
      tweets.save()
      return redirect('tweet_list')
  else:
    form=tweetforms()
  return render(request,'tweet/tweet_form.html',{'form':form})
@login_required
def edit(request,tweet_id):
  tweets=get_object_or_404(tweet,pk=tweet_id,user=request.user)
  if request.method=='POST':
    form=tweetforms(request.POST,request.FILES,instance=tweets)
    if form.is_valid():
      tweets=form.save(commit=False)
      tweets.user=request.user
      tweets.save()
      return redirect('tweet_list')
  else:
    form=tweetforms(instance=tweets)
    return render(request,'tweet/tweet_form.html',{'form':form})
@login_required
def delete(request,tweet_id):
  tweets=get_object_or_404(tweet,pk=tweet_id)
  if request.method=='POST':
    tweets.delete()
    return redirect('tweet_list')
  return render(request,'tweet/tweet_delete.html',{'tweets':tweets})
# def register(request):
#   form=UserRegistration(request.POST,request.FILES)
#   if form.is_valid():
#     user=form.save(commit=False)
#     user.set_password(form.cleaned_data['password1'])
#     user.save()
#     login(request,user)
#     return redirect('tweet_list')
#   else:
#     form=UserRegistration()
#     return render(request,'registration/form_register.html',{'form':form})
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistration(request.POST, request.FILES)
#         if form.is_valid():
#             emails=form.cleaned_data['email']
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
            
#             # Check if the user already exists
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists. Please choose another one.')
#                 return render(request, 'registration/form_register.html', {'form': form})
#             elif User.objects.filter(email=emails).exists():
#                messages.error(request, 'Email already registered. Please choose another one.')
#                return render(request, 'registration/form_register.html', {'form': form})

#             user = form.save(commit=False)
#             user.set_password(password) 
#             user.save()  

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)  
#                 return redirect('tweet_list')  
#             else:
#                 messages.error(request, 'Authentication failed. Please try again.')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = UserRegistration() 
#     return render(request, 'registration/form_register.html', {'form': form})  
def register(request):
  if request.method=='POST':
    form=UserRegistration(request.POST,request.FILES)
    if form.is_valid():
      emails=form.cleaned_data['email']
      username=form.cleaned_data['username']
      password=form.cleaned_data['password1']
      if User.objects.filter(username=username).exists():
        messages.error(request,'Username alredy Exists,Please Choose a Different one.')
        return render(request,'registration/form_register.html',{'form':form})
      elif User.objects.filter(email=emails).exists():
        messages.error(request,'Email already registered,Please Choose a Different one.')
        return render(request,'registration/form_register.html',{'form':form})
      users=form.save(commit=False)
      users.set_password(password)
      users.save()
      if users is not None:
        login(request,users)
        return redirect('tweet_list')
      else:
        messages.error(request,"Username  oPassword doesn't match.")
    else:
      messages.error(request,'Invalid Username or Password.') 
  else:
    form=UserRegistration()
  return render(request,'registration/form_register.html',{'form':form})
def profile(request,user_id):
  user=get_object_or_404(User,pk=user_id)
  tweets=tweet.objects.all().filter(user=user).order_by('-created_at')
  # pho_user=photo.objects.get(user=user).first()
  try:
    pho1=photo.objects.get(user=user)
  except photo.DoesNotExist:
    pho1=None
  try:
    pu=premium_user.objects.filter(user=user).last()
  except premium_user.DoesNotExist:
    pu=None
  return render(request,'tweet/profile.html',{'pho1':pho1,'tweets':tweets,'pu':pu})
  
def ph_edit(request,pho_id):
  pho_user=get_object_or_404(photo,pk=pho_id)
  if request.method=='POST':
    form=photo_form(request.POST,request.FILES,instance=pho_user)
    if form.is_valid():
      pho=form.save(commit=False)
      pho.user=request.user
      form.save()
      return redirect('tweet_list')
  else:
    form=photo_form(instance=pho_user)
    return render(request,'tweet/photo_edit.html',{'form':form})
def create_pic(request):
  if request.method=='POST':
    form=photo_form(request.POST,request.FILES)
    if form.is_valid():
      ph=form.save(commit=False)
      ph.user=request.user
      ph.save()
      return redirect('tweet_list')
  else:
    form=photo_form()
  return render(request,'tweet/photo_create.html',{'form':form})
def premium(request):
  p_user, created = premium_user.objects.get_or_create(user=request.user)
  client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
  payment=client.order.create({'amount':10000,'currency':'INR','payment_capture':1 })
  if('id' in payment ):
    p_user.razor_pay_order_id = payment['id']
    p_user.save()
    # return redirect('profile',user_id=request.user.id)
  context={'user':request.user,'payment':payment}
  return render(request,'tweet/premium.html',context)
def set_p_user(request):
  if request.method=='POST':
    form=pu_form(request.POST)
    if(form.is_valid()):
      pu=form.save(commit=False)
      pu.user=request.user
      pu.save()
      return redirect('premium')
    else:
      form=pu_form()
    return render(request,'tweet/profile.html',{'form':form})
  

