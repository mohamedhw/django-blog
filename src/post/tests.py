from urllib import response
from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from .models import Post, PostComments
from django.contrib.auth.models import User
import json
from post.views import (
    detailview,
    PostCreateView,
    HomeView,     
    PostDeleteView,
    PostUpdateView,
    UserPostsView,
    saved_posts
)

class TestUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('post:list')
        self.assertEquals(resolve(url).func.view_class, HomeView)


    def test_list_url_resolves(self):
        url = reverse('post:create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)


    def test_list_url_resolves(self):
        url = reverse('post:detail', args=[15])
        self.assertEquals(resolve(url).func, detailview)


    def test_list_url_resolves(self):
        url = reverse('post:delete', args=[15])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)


    def test_list_url_resolves(self):
        url = reverse('post:update', args=[15])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)


    def test_list_url_resolves(self):
        url = reverse('post:user-posts', args=["mohamed"])
        self.assertEquals(resolve(url).func.view_class, UserPostsView)




class TestViews(TestCase):

    def setUp(self):


        user = User.objects.create(username = 'testuser')
        user.set_password("testpw")
        user.save()

        self.client = Client()
        self.client.login(username = "testuser", password = 'testpw')

        post1 = Post.objects.create(pk = '15', body = 'test', author = user)




        self.list_url = reverse('post:list')
        self.detail_url = reverse('post:detail', args=[15])
        self.user_posts_url = reverse('post:user-posts', args=[user])
        self.delete_url = reverse('post:delete', args=[15])


    def test_list_view_GET(self):


        response = self.client.get(self.list_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/post_list_temp.html')



    def test_detail_view_GET(self):


        response = self.client.get(self.detail_url)


        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/post_detail.html')


    def test_user_posts_view_GET(self):

        response = self.client.get(self.user_posts_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'post/user_post_list.html')

    def test_delete_view_POST(self):

        response = self.client.delete(self.delete_url)
        response2 = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response2.status_code, 404)