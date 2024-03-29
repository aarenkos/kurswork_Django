from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, ResetView, ResetDoneView, EmailVerifyDoneView, EmailVerifySendedView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('done/', ResetDoneView.as_view(), name='done'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify-sended/', EmailVerifySendedView.as_view(), name='email_verify_sended'),
    path('email-verify-done/<str:uidb64>/<str:token>/', EmailVerifyDoneView.as_view(), name='email_verify_done')
]