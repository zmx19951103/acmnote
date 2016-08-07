from django.shortcuts import render
from .models import ClassicNote
from django.http import Http404, HttpResponseNotAllowed,HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test, login_required
from authentication.models import MyUser
from util.verification import user_check
# Create your views here.
from .forms import ClassicNoteForm
from problem.models import Problem
from .tables import ClassicNoteTable

from dal import autocomplete
from .models import NoteTag


class NoteTagAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.has_add_permission:
            return NoteTag.objects.none()
        qs = NoteTag.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def create_object(self, text):
        """Create an object given a text."""
        if not self.has_add_permission:
            raise PermissionDenied
        user = self.request.user if self.request.user.is_authenticated() else None
        my_user = MyUser.objects.get(user=user) if user else None
        return self.get_queryset().create(**{self.create_field: text,
                                             'create_user': my_user})


def note_list_page(request):
    """
    前台的笔记列表
    """
    # 正常情况
    notes = ClassicNoteTable()
    content = {
        'notes': notes,
    }
    return render(request, 'note/note_list.html', content)


def note_page(request, note_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        note = ClassicNote.objects.get(pk=note_id)
    except ClassicNote.DoesNotExist:
        raise Http404(u"笔记不存在")
    editable = False
    if my_user:
        if my_user.pk == note.author.pk:
            editable = True
    content = {
        'user': my_user,
        'note': note,
        'editable': editable,
    }
    return render(request, 'note/note_page.html', content)


@user_passes_test(user_check)
def edit_note(request, note_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        note = ClassicNote.objects.get(pk=note_id)
    except ClassicNote.DoesNotExist:
        raise Http404(u"笔记不存在")
    if not my_user or note.author != my_user:
        raise PermissionDenied
    if request.method == 'POST':
        form = ClassicNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            content = {
                'note': note,
                'editable': True,
            }
            return render(request, 'note/note_page.html', content)
        else:
            content = {
                'form': form,
                'note': note,
            }
            return render(request, 'note/edit_note.html', content)
    else:
        form = ClassicNoteForm(instance=note)
        content = {
            'form': form,
            'note': note,
        }
        return render(request, 'note/edit_note.html', content)


@user_passes_test(user_check)
def add_note(request, problem_id):
    user = request.user if request.user.is_authenticated() else None
    my_user = MyUser.objects.get(user=user) if user else None
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        raise Http404(u"题目不存在")
    if request.method == 'POST':
        form = ClassicNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = my_user
            note.problem = problem
            content = {
                'note': note,
                'editable': True,
            }
            note.save()
            return render(request, 'note/note_page.html', content)
        else:
            content = {
                'form': form,
                'problem': problem
            }
            return render(request, 'note/edit_note.html', content)
    else:
        form = ClassicNoteForm()
        content = {
            'form': form,
            'problem': problem
        }
        return render(request, 'note/add_note.html', content)



