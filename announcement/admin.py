from django.contrib import admin
from .models import Announcement
# Register your models here.
@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_time')
    list_display_links = ('title',)