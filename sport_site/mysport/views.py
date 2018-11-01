from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.views.generic import UpdateView,ListView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from mysport.models import Board,Topic,Post
from mysport.forms import NewTopicForm,PostForm

def home(request):
	boards = Board.objects.all()
	return render(request,'home.html',{'boards' : boards})
# 使用CBV模型列表重写home
class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'home.html'

def board_topics(request,pk):
	board = get_object_or_404(Board,pk=pk)
	queryset = board.topics.order_by('-last_update')
	# 从前端获取当前的页码数,默认为1
	page = request.GET.get('page',1)
	#生成paginator对象,定义每页显示20条记录
	paginator = Paginator(queryset,20)

	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		# 如果用户输入的页码不是整数时,显示第1页的内容
		topics = paginator.page(1)
	except EmptyPage:
		# 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
		topics = paginator.page(paginator.num_pages)
	return render(request,'topics.html',{'board': board,'topics': topics})

@ login_required
def new_topic(request,pk):
	board = get_object_or_404(Board,pk=pk)
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board

			# 将发布主题的用户设置当前登录的用户
			topic.starter = request.user 
			topic.save()

			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by = request.user
				)
			return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
	else:
		form = NewTopicForm()
	return render(request,'new_topic.html',{'board': board, 'form': form})

class PostListView(ListView):
	models = Post
	context_object_name = 'posts'
	template_name = 'topic_posts.html'
	paginate_by = 2 # 每页只显示2个创建时间最近的post的回复

	def get_context_data(self,**kwargs):
		# 不希望相同的用户再次刷新页面的时候被统计为多次访问。为此，我们可以使用会话(sessions)
		session_key = 'viewed_topic_{}'.format(self.topic.pk)
		if not self.request.session.get(session_key,False):
		# 若存在会话则返回该会话，否则返回NULL，这样的作用是防止一次访问记录多次view
			self.topic.views += 1
			self.topic.save()
			self.request.session[session_key] = True
		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.topic = get_object_or_404(Topic,board__pk=self.kwargs.get('pk'),pk=self.kwargs.get('topic_pk'))
		queryset = self.topic.posts.order_by('created_at')
		return queryset

@login_required
def reply_topic(request,pk,topic_pk):
	topic = get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.topic = topic
			post.created_by = request.user
			post.save()
			
			# 记录最近一次topic的更新时间
			topic.last_update = timezone.now()
			topic.save()

			# 回复之后返回到topic_posts的页面首页
			# return redirect('topic_posts',pk=pk,topic_pk=topic_pk)
			
			# 回复之后返回到topic_posts的页面的最后一页
			# reverse反解析topic_posts的url,并且补充上pk和topic_pk的信息
			topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
			topic_post_url = '{url}?page={page}#{id}'.format(
				url=topic_url,
				id=post.pk,
				page=topic.get_page_count()
			)

			return redirect(topic_post_url)
			
	else:
		form = PostForm
	return render(request,'reply_topic.html',{'topic':topic,'form':form})

# 将使用 GCBV 来实现编辑帖子的视图
# 我们不能用 @login_required 装饰器直接装饰类。
# 我们必须使用一个工具@method_decorator，并传递一个装饰器（或一个装饰器列表）并告诉应该装饰哪个类。
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
	model = Post
	fields = ('message',)
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	# 如果我们没有设置context_object_name 来发布,它将可以被用作：object.topic.board.pk
	context_object_name = 'post'

	# 重写UpdateView的get_queryset方法,可以解决其他用户可以编辑所有帖子的问题
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by=self.request.user)

	def form_valid(self,form):
		post = form.save(commit=False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)



