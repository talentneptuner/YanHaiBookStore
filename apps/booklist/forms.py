from django import forms

from .models import BookList


class BookListForm(forms.ModelForm):
    class Meta:
        model = BookList
        fields = ['cover','title','tag1']