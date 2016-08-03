from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import *


class ProblemAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'oj_all', 'title', 'hint', 'create_time',
                    'difficulty_rank', 'difficulty_num', )
    list_display_links = ('pk', 'oj_all',)
    search_fields = ('oj', 'title',)


class ProblemTagAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'name', 'create_time',)
    list_display_links = ('pk', 'name',)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemTag, ProblemTagAdmin)
