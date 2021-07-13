from django.contrib import admin
from .models import Post, PostComments



admin.site.register(Post)
admin.site.register(PostComments)