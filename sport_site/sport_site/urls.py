"""sport_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

# 用户登录和突出所需
from django.contrib.auth import views as auth_views

# 配置media
from django.views.static import serve
from django.conf.urls.static import static
from sport_site.settings import MEDIA_ROOT,MEDIA_URL

from mysport import views
from accounts import views as accounts_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.BoardListView.as_view()),
    url(r'^home/$',views.home,name='home'),

    url(r'^boards/(?P<pk>\d+)/$',views.board_topics,name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$',views.new_topic,name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$',views.PostListView.as_view(), name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$',views.reply_topic,name='reply_topic'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
    	views.PostUpdateView.as_view(), name='edit_post'),

    # 用户管理相关url
    url(r'^signup/$',accounts_views.signup,name='signup'),
    url(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    # 带有表单的页面，用于启动重置过程
    url(r'^reset/$',
		auth_views.PasswordResetView.as_view(
			template_name='password_reset.html',
			email_template_name='password_reset_email.html',
			subject_template_name='password_reset_subject.txt'),
		name='password_reset'),
    # 一个成功的页面，表示该过程已启动，指示用户检查其邮件文件夹等
	url(r'^reset/done/$',
		auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
		name='password_reset_done'),
	# 检查通过电子邮件发送token的页面,密码确认url0
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
		name='password_reset_confirm'),
	# 一个告诉用户重置是否成功的页面
	url(r'^reset/complete/$',
		auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
		name='password_reset_complete'),

	# 此视图旨在提供给希望更改其密码的登录用户使用。通常，这些表单由三个字段组成：旧密码、新密码、新密码确认。
	url(r'^settings/password/$',auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
		name='password_change'),
	url(r'^settings/password/done/$',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
    	name='password_change_done'),
	url(r'^settings/account/$',accounts_views.UserUpdateView.as_view(),name='my_account'),

	# 配置media
	url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT})
] + static(MEDIA_URL,document_root=MEDIA_ROOT)
