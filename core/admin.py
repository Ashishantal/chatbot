from django.contrib import admin

# Register your models here.

from .models import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'time', 'extract')  # Fields shown in admin list view
    readonly_fields = ('time', 'extract')       # Make extract and time read-only
