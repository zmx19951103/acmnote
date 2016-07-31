from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from problem.models import *
from django_summernote.admin import SummernoteModelAdmin


class MyUserInline(admin.StackedInline):
    model = MyUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (MyUserInline,)


class ProblemTagAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'name', 'create_time',)
    list_display_links = ('pk', 'name',)


class ProblemAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'oj_all', 'title', 'hint', 'create_time', 'last_update_time',
                    'difficulty_rank', 'difficulty_num', )
    list_display_links = ('pk', 'oj_all',)
    search_fields = ('oj', 'title',)


class NoteAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'ordinal', 'pub_time', 'update_time', )
    list_display_links = ('pk', 'ordinal', )


class RelationAdmin(SummernoteModelAdmin):
    list_display = ('pk', 'people', 'problem', 'AC_time', 'difficulty', )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(ProblemTag, ProblemTagAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Relation, RelationAdmin)
