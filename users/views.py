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

from users.forms import UserRegisterForm, PasswordAltResetForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


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


class EmailVerifyView(FormView):
    model = User
    email_template_name = "users/email_verify_message.html"
    template_name = 'users/email_verify_confirm.html'
    success_url = 'users/email_verify_sended.html'
    token_generator = default_token_generator

    @staticmethod
    def send_mail_for_verify(request, user, token_generator):
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator.make_token(user),
        }
        message = render_to_string('users/email_verify_message.html', context=context)
        email = EmailMessage(
            'Подтверждение электронной почты',
            message,
            to=[user.email],
        )
        email.send()

    def get(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        user = request.user
        self.send_mail_for_verify(request, user, self.token_generator)
        return render(request, self.success_url)


class EmailVerifyDoneView(View):
    model = User
    template_name = 'users/email_verify_done.html'
    unsuccessful_template_name = 'users/email_verify_unsuccessful.html'
    anonim_template_name = 'users/email_verify_anonim.html'
    token_generator = default_token_generator

    @staticmethod
    def get_user(model, uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = model.objects.get(pk=uid)
        except (
                TypeError,
                ValueError,
                OverflowError,
                model.DoesNotExist,
                ValidationError,
        ):
            user = None
        return user

    def get(self, request, uidb64, token, **kwargs):
        user = request.user
        print(user.pk)

        if user.pk is None:
            return render(request, self.anonim_template_name)

        user_for_email_activation = self.get_user(self.model, uidb64)
        token_for_email_activation = self.token_generator.check_token(user, token)

        if user == user_for_email_activation and token_for_email_activation:
            user.is_email_active = True
            user.save()
            return render(request, self.template_name)
        else:
            return render(request, self.unsuccessful_template_name)