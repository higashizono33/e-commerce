from django.shortcuts import render, redirect, HttpResponseRedirect
# from django.contrib.auth.models import User
from .forms import UserCreateForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, get_user_model

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {
                'form': form,
            }    
    else:
        form = UserCreateForm()
        context = {
            'form': form,
        }
    return render(request, 'registration/signup.html', context)

class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    def form_valid(self, form):
        login(self.request, form.get_user())
        self.request.session['userId'] = form.get_user().id
        if form.get_user().is_superuser:
            return redirect('dashboard')
        else:
            return HttpResponseRedirect(self.get_success_url())
