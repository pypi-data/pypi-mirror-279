from django.db import models
from django import forms

from wang_editor.widgets import WangEditorWidget


class WangEditorField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'form_class': WangEditorFormField}
        defaults.update(kwargs)
        return super(WangEditorField, self).formfield(**defaults)


class WangEditorFormField(forms.fields.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget': WangEditorWidget(),
        })
        super(WangEditorFormField, self).__init__(*args, **kwargs)
