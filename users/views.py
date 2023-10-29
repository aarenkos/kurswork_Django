# from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, FormView
import re
from users.forms import UserRegisterForm, PasswordAltResetForm
from users.models import User
from django.http import HttpResponse

# Create your views here.
from django.contrib.auth.tokens import default_token_generator

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        token_generator = default_token_generator
        user.save()
        token = token_generator.make_token(user)
        user.token = token
        user.save()
        current_site = get_current_site(self.request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        }
        message = render_to_string('users/email_verify_message.html', context=context)
        email = EmailMessage(
            'Подтверждение электронной почты',
            message,
            to=[user.email],
        )
        email.send()
        return response


class ResetView(FormView):
    model = User
    form_class = PasswordAltResetForm
    email_template_name = 'users/reset_email.html'
    template_name = 'users/reset_password.html'
    success_url = reverse_lazy('users:done')
    token_generator = default_token_generator

    def get(self, request, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    @staticmethod
    def send_mail_for_reset(request, email, new_password):
        current_site = get_current_site(request)
        context = {
            'domain': current_site.domain,
            'new_password': new_password
        }
        message = render_to_string('users/reset_email.html', context=context)
        email = EmailMessage(
            'Восстановление пароля',
            message,
            to=[email],
        )
        email.send()

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = self.model.objects.get(email=email)
            if user:
                new_password = self.token_generator.make_token(user)[:10]
                user.set_password(new_password)
                user.save()
                self.send_mail_for_reset(request, email, new_password)
                return redirect(self.success_url)
            else:
                return render(request, 'users/email_verify_unsuccessful.html')


class ResetDoneView(PasswordResetDoneView):
    template_name = 'users/reset_done.html'
    title = "Сообщение отправлено!"


class EmailVerifyDoneView(View):
    template_name = 'users/email_verify_done.html'
    unsuccessful_template_name = 'users/email_verify_unsuccessful.html'
    token_generator = default_token_generator

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            User = get_user_model()
            user = User.objects.get(pk=uid)
            token = user.token
            return user, token
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return None

    def get(self, request, uidb64, token, **kwargs):
        user, token = self.get_user(uidb64)
        # print(user)
        # print(token)
        url = request.build_absolute_uri()
        print (url)
        if not user:
            print('Пользователь не найден')
            return HttpResponse('Пользователь не найден')
        url_split = url.split('/')
        print(url_split)
        user_token = url_split[-2]
        print(user_token)
        if user.is_email_active:
            return HttpResponse('Уже подтвержден')
        if user_token == token:
            user.is_email_active = True
            user.save()
            return render(request, self.template_name)
        else:
            # Токен недействителен или пользователь не найден
            return render(request, self.unsuccessful_template_name)
