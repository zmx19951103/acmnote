# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

from datetimewidget.widgets import DateTimeWidget
from django.core.exceptions import  *

from .models import *
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class ProblemTagForm(forms.ModelForm):
    # intro = forms.CharField(label='介绍', widget=SummernoteInplaceWidget())
    intro = forms.CharField(label='介绍', widget=SummernoteWidget(attrs={'width': '100%'}))

    def clean(self):
        cleaned_data = super(ProblemTagForm, self).clean()
        intro = cleaned_data.get('intro')
        name = cleaned_data.get('name')
        abbreviation = cleaned_data.get('abbreviation')
        if not intro:
            msg = "Tag's Introduce should not be empty!"
            self.errors['intro'] = self.error_class([msg])
        if not name:
            msg = "Tag's name should not be empty!"
            self.errors['name'] = self.error_class([msg])
        if not abbreviation:
            msg = "Tag's short name should not be empty!"
            self.errors['abbreviation'] = self.error_class([msg])
        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data['name']
        try:
            ProblemTag.objects.get(name=name)
        except ObjectDoesNotExist:
            return name
        raise forms.ValidationError('Exist tag full name!')

    def clean_abbreviation(self):
        abbreviation = self.cleaned_data['abbreviation']
        try:
            ProblemTag.objects.get(abbreviation=abbreviation)
        except ObjectDoesNotExist:
            return abbreviation
        raise forms.ValidationError("Exist tag's short name!")

    class Meta:
        model = ProblemTag
        fields = '__all__'
        exclude = ['slug']


class NoteForm(forms.ModelForm):
    SCORE_CHOICE = zip(range(1, 11), range(1, 11))
    difficulty = forms.TypedChoiceField(choices=SCORE_CHOICE, label='Difficult Num', )
    ac_time = forms.DateTimeField(label='AC时间', initial="", required=False,
                                  widget=DateTimeWidget(usel10n=True, bootstrap_version=3))

    content = forms.CharField(label='content', widget=SummernoteWidget(attrs={'width': '100%'}))

    def clean(self):
        cleaned_data = super(NoteForm, self).clean()
        ac_time = cleaned_data.get('ac_time')
        content = cleaned_data.get('content')
        if ac_time:
            if ac_time >= now():
                msg = "AC time is invalid!"
                self.errors['ac_time'] = self.error_class([msg])
        if not content:
            msg = "Content should not be empty!"
            self.errors['content'] = self.error_class([msg])
        return cleaned_data

    class Meta:
        model = Note
        fields = '__all__'
        exclude = ['problem', 'author']

