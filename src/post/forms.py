from django import forms
from .models import PostComments, Post
from django.contrib.auth.models import User


class CommentsFrom(forms.ModelForm):
    # content = forms.CharField(max_length=100, required=True,
    #     widget=forms.TextInput(
    #         attrs= {
    #                 "cols": 120,
    #                 "placeholder": "enter the description",
    #                 "rows": 20,
    #             }
    #         )
    #     )


    class Meta:
        model  = PostComments
        fields = {
            'comment'
        }
