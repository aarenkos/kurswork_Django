from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_active')
    readonly_fields = ('email', 'phone', 'avatar', 'is_email_active', 'password', 'country', 'last_login',
                       'is_superuser', 'groups', 'user_permissions', 'first_name', 'last_name', 'is_staff',
                       'date_joined')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.exclude(is_superuser=True)