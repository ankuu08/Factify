from django.urls import path,include
from . import views
from django.contrib.auth.urls import views as auth_view
urlpatterns = [
    path('',views.tweet_list,name='tweet_list'),
    path('<int:tweet_id>/edit/',views.edit,name="tweet_edit"),
    path('create/',views.create,name='tweet_create'),
    path('<int:tweet_id>/delete/',views.delete,name='tweet_delete'),
    path('register/',views.register,name='register'),
    path('<int:user_id>/profile',views.profile,name='profile'),
    path('<int:pho_id>/edit_profile',views.ph_edit,name='ph_edit'),
    path('pic/',views.create_pic,name='create_pic'),
    path('set_pu/',views.set_p_user,name='set_pu'),
    path('premium/',views.premium,name="premium"),
    path("chatbot/",views.chatbot,name='chatbot'),
]