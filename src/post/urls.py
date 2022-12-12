from django.urls import path
from .views import (
    HomeView,
    #PostDetailview,
    PostCreateView,
    PostDeleteView,
    PostUpdateView,
    UserPostsView,
    #createcomment,
    searchpost,
    #CommentCreateView,
    #CommentView,
    detailview,
    like_button,
    add_comment,
    aj_comments,
    aj_get_comment,
    save_button,
    saved_posts,
    )

from . import api


app_name = 'post'

urlpatterns = [
    path('', HomeView.as_view(), name='list'),
    path('user/<str:username>/', UserPostsView.as_view(), name='user-posts'),
    #path('<int:pk>', PostDetailview.as_view(), name="detail"),
    path('create/', PostCreateView.as_view(), name="create"),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name="delete"),
    path('<int:pk>/update/', PostUpdateView.as_view(), name="update"),
    path('search/', searchpost, name="search"),
    #path('<int:pk>/comment/<str:username>/', CommentCreateView.as_view(), name="comment-create"),
    #path('comments/', CommentView.as_view(), name="comment"),
    path('<int:pk>', detailview, name="detail"),
    path('<int:pk>/comment/', add_comment, name="add-comment"),
    #path('<int:pk>/comment/', createcomment),
    path('api-list/', api.ApiPostList.as_view(), name="api_view"),
    path('api-list/<int:pk>/', api.post_detail_api, name="api_detail"),
    path('<int:pk>/like/', like_button, name="like"),
    path('comment/', aj_comments),
    path('<int:pk>/get/', aj_get_comment, name="get"),
    path('<int:pk>/saved/', save_button, name="save"),
    path('save/', saved_posts, name="saved")
]
