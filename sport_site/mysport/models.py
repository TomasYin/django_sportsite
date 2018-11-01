import math

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe

from markdown import markdown

class Board(models.Model):
	name = models.CharField(max_length=30,unique=True)
	description = models.CharField(max_length=100)

	def __str__(self):
		return self.name

	def get_posts_count(self):
		# 双下划线的topic__board用于通过模型关系来定位，在内部，Django 在 Board-Topic-Post之间构建了桥梁，构建SQL查询来获取属于指定版块下面的帖子回复
		return Post.objects.filter(topic__board=self).count()

	def get_last_post(self):
		# 得到最近的一条帖子的时间
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
	subject = models.CharField(max_length=255)
	last_update = models.DateTimeField(auto_now_add=True)
	board = models.ForeignKey(Board,related_name='topics')
	starter = models.ForeignKey(User,related_name='topics')
	views = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.subject

	def get_replies_count(self):
		# 计算reply的数量
		return Post.objects.filter(topic_id=self.id).count()
	
	# 在主题列表中提供一个更好一点的导航
	def get_page_count(self):
		count = self.posts.count()
		# 2指的是分页的时候每页的数据的数量
		pages = count / 2
		return math.ceil(pages)
	def has_many_pages(self,count=None):
		if count is None:
			count = self.get_page_count()
		return count>6
	def get_page_range(self):
		count = self.get_page_count()
		if self.has_many_pages(count):
			return range(1,5)
		return range(1,count+1)

	def get_last_ten_posts(self):
		# 在reply页面中限制在显示最近的十个回复
		return self.posts.order_by('-created_at')[:10]


class Post(models.Model):
	message = models.TextField(max_length=4000)
	topic = models.ForeignKey(Topic,related_name='posts')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	created_by = models.ForeignKey(User,related_name='posts')
	updated_by = models.ForeignKey(User,null=True,related_name='+')

	def __str__(self):
		# 使用了 Truncator 工具类，这是将一个长字符串截取为任意长度字符的简便方法
		truncated_message = Truncator(self.message)
		return truncated_message.chars(30)

	def get_message_as_markdown(self):
		# 当使用 Mardown 功能时，我们需要先让它转义一下特殊字符，然后再解析出 Markdown 标签。这样做之后，输出字符串可以安全的在模板中使用。
		return mark_safe(markdown(self.message, safe_mode='escape'))

