from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, ResetView, ResetDoneView, EmailVerifyView, EmailVerifyDoneView

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('reset/', ResetView.as_view(), name='reset'),
    path('done/', ResetDoneView.as_view(), name='done'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email_verify/', EmailVerifyView.as_view(), name='email_verify'),
    path('email_verify_done/<uidb64>/<token>/', EmailVerifyDoneView.as_view(), name='email_verify_done')
]