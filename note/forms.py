# -*- coding: utf-8 -*-
from django import forms
from django.utils.timezone import now
from django.contrib.auth.models import User
from datetimewidget.widgets import DateTimeWidget
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from .models import *
from dal import autocomplete


class ClassicNoteForm(forms.ModelForm):
    ac_time = forms.DateTimeField(label='AC时间', initial="", required=False,
                                  widget=DateTimeWidget(usel10n=True,
                                                        bootstrap_version=3,
                                                        attrs={'width': '100%'})
                                  )
    SCORE_CHOICE = zip(range(1, 11), range(1, 11))
    difficulty = forms.TypedChoiceField(choices=SCORE_CHOICE,
                                        label='难度系数',
                                        coerce=int
                                        )
    content = forms.CharField(label='笔记内容',
                              widget=SummernoteWidget(attrs={'width': '100%'}))

    def clean(self):
        cleaned_data = super(ClassicNoteForm, self).clean()
        ac_time = cleaned_data.get('ac_time')
        content = cleaned_data.get('content')
        difficulty = cleaned_data.get('difficulty')
        if ac_time:
            if ac_time >= now():
                msg = "AC time is invalid!"
                self.errors['ac_time'] = self.error_class([msg])
        if not content:
            msg = "Content should not be empty!"
            self.errors['content'] = self.error_class([msg])
        if not difficulty or difficulty < 1 or difficulty > 10:
            msg = "难度值的范围需要在[1,10]区间内！"
            self.errors['difficulty'] = self.error_class([msg])
        return cleaned_data

    class Meta:
        widgets = {
            'tags': autocomplete.ModelSelect2Multiple(
                url='note-tag-autocomplete')
        }
        labels = {
            'tags': '标签',

        }
        model = ClassicNote
        fields = '__all__'

        exclude = ['problem', 'author']

