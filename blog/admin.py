from django.contrib import admin

from blog.models import Blog


# Register your models here.
@admin.register(Blog)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_created')
    readonly_fields = ('date_created', 'view_counter')