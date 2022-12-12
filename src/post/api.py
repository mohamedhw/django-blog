from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post
from rest_framework.decorators import api_view
from rest_framework import generics



# @api_view(['GET'])
# def postlistapi(request):
#     all_posts = Post.objects.all()
#     data = PostSerializer(all_posts, many=True).data
#     return Response({'data':data})

@api_view(['GET'])
def post_detail_api(request, pk):
    detail_post = Post.objects.get(pk=pk)
    data = PostSerializer(detail_post).data
    return Response({'data':data})

class ApiPostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()