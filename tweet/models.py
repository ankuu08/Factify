from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class tweet(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)
  Text=models.TextField(max_length=240)
  photo=models.ImageField(upload_to='photos/',blank=True,null=True)
  created_at=models.DateTimeField(auto_now_add=True)
  updated_at=models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.user.username}-{self.Text[:10]}'
class photo(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE);
  user_photo=models.ImageField(upload_to='user_photo/',null=True,blank=True)

  def __str__(self):
    return self.user.username
class premium_user(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  is_premium=models.BooleanField(default=False)
  razor_pay_order_id=models.CharField(max_length=100,null=True,blank=True)
  razor_pay_payment_id=models.CharField(max_length=100,null=True,blank=True)
  razor_pay_payment_signature=models.CharField(max_length=100,null=True,blank=True)

  def __str__(self):
    return self.user.username


 