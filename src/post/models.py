from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q    



# def image_upload(instance, filename):
#     imagename , ext = filename.split(".")
    
#     return "post_images/%s.%s"%(instance.date,ext)


class PostManager(models.Manager):

    def search(self, query=None):
        if query is None or query == "":
            self.get_queryset().none()

        lookups = Q(body__icontains=query)
        return self.get_queryset().filter(lookups)

class Post(models.Model):
    body       = models.TextField()
    date       = models.DateTimeField(default=timezone.now)
    author     = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    image      = models.ImageField(upload_to="post_images", blank=True, null=True)
    like       = models.ManyToManyField(User, blank=True, related_name="like_button")
    like_count = models.BigIntegerField(default='0')
    save_post  = models.ManyToManyField(User, blank=True, related_name="save_post")

    objects = PostManager()
    def __str__(self):
        return self.body
        
    def get_absolute_url(self):
        return reverse('post:detail' , kwargs={'pk': self.pk})


class PostComments(models.Model):
    post    = models.ForeignKey(Post, on_delete=models.CASCADE)
    author  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.TextField()
    date    = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.author.username)