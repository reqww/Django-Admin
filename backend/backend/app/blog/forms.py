from django.forms import ModelForm
from django import forms

from .models import Post


class PostForm(ModelForm):
    title = forms.CharField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
    picture = forms.ImageField(required=False)
    id = forms.IntegerField(required=False)
    draft = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = "__all__"
