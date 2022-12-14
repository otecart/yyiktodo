from django import forms

from .models import Entry


class EntryForm(forms.ModelForm):
    text = forms.CharField(
        min_length=2,
        max_length=200,
        label="",
    )

    class Meta:
        model = Entry
        fields = ["text"]
