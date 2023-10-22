from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import CreateMailingView, ListMailingView, UpdateMailingView, DeleteMailingView, \
    DetailMailingView, CreateClientView, ListClientView, DeleteClientView, MailingLogListView, DeleteMailingLogView, \
    DetailMailingLogView

app_name = 'mailing'

urlpatterns = [
    path('create_mailing/', CreateMailingView.as_view(), name='create_mailing'),
    path('list_mailing/', cache_page(60)(ListMailingView.as_view()), name='list_mailing'),
    path('update_mailing/<int:pk>/', UpdateMailingView.as_view(), name='update_mailing'),
    path('delete_mailing/<int:pk>/', DeleteMailingView.as_view(), name='delete_mailing'),
    path('detail_mailing/<int:pk>/', DetailMailingView.as_view(), name='detail_mailing'),
    path('create_client/', CreateClientView.as_view(), name='create_client'),
    path('clients_list/', ListClientView.as_view(), name='clients_list'),
    path('delete_client/<int:pk>/', DeleteClientView.as_view(), name='delete_client'),
    path('mailing_logs_list/', MailingLogListView.as_view(), name='mailing_logs_list'),
    path('mailing_log_detail/<int:pk>/', DetailMailingLogView.as_view(), name='mailing_log_detail'),
    path('delete_mailing_log/<int:pk>/', DeleteMailingLogView.as_view(), name='delete_mailing_log'),
]