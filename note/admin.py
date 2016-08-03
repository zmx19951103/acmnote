from django.contrib import admin

# Register your models here.
from .models import ClassicNote
from django_summernote.admin import SummernoteModelAdmin


class ClassicNoteAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'ordinal', 'pub_time', 'update_time', )
    list_display_links = ('pk', 'ordinal', )

admin.site.register(ClassicNote, ClassicNoteAdmin)
