from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.forms import SignUpForm,UserProfileForm


def signup(request):
	if request.method == 'POST':
		# 使用django自带的UserCreationForm
		# form = UserCreationForm(request.POST)

		form = SignUpForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if form.is_valid() and profile_form.is_valid():
			user = form.save()
			auth_login(request,user)

			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			return redirect('home')
	else:
		# form = UserCreationForm()

		form = SignUpForm()
		profile_form = UserProfileForm()
	return render(request,'signup.html',{'form':form,'profile_form':profile_form})

@method_decorator(login_required,name='dispatch')
class UserUpdateView(UpdateView):
	model = User
	fields = ('first_name','last_name','email')
	template_name = 'my_account.html'
	success_url = reverse_lazy('my_account')

	def get_object(self):
		return self.request.user

