from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import View
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from core.settings import GOOGLE_CALLBACK_ADDRESS
from src.accounts.forms import UserProfileForm


@method_decorator(login_required, name='dispatch')
class CrossAuthView(View):

    def get(self, request):
        if request.user.is_superuser:
            return redirect('admins:dashboard')
        elif request.user.is_instructor:
            return redirect('instructor:dashboard')
        else:
            return redirect('student:dashboard')


@method_decorator(login_required, name='dispatch')
class UserUpdateView(View):

    def get(self, request):
        form = UserProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            messages.success(request, "Your profile updated successfully")
            form.save(commit=True)
        context = {'form': form}
        return render(request, template_name='accounts/user_update_form.html', context=context)


""" API """


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = GOOGLE_CALLBACK_ADDRESS


@method_decorator(login_required, name='dispatch')
class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('accounts:administration-login')



