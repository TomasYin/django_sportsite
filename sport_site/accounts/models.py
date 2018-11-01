from django.db import models
from django.contrib.auth.models import User

# 设置每个用户的用户名相对应的头像的名称，filename可以将图片名重置
def user_picture(instance,filename):
    return '/'.join(['user_picture', str(instance.user.username)]) + '.jpg'
class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
	picture = models.ImageField(upload_to=user_picture,default='user_picture/default.jpg', verbose_name='头像',blank=True)

	def __str__(self):
		return self.user.username