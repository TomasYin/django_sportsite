import hashlib
from urllib.parse import urlencode

from django import template
from django.conf import settings

"""
给用户个人信息添加图片的一种非常简单的方法就是使用 Gravatar
"""
register = template.Library()


@register.filter
def gravatar(user):
	email = user.email.lower().encode('utf-8')
	default = 'mm'
	size = 256
	url = 'https://www.gravatar.com/avatar/{md5}?{params}'.format(
		md5=hashlib.md5(email).hexdigest(),
		params=urlencode({'d': default, 's': str(size)})
	)
	return url