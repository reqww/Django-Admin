from rest_framework.generics import ListAPIView, CreateAPIView

# from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.renderers import BrowsableAPIRenderer

from .serializers import PostSerializer
from .models import Post


class PostListView(ListAPIView, CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    renderer_classes = [CamelCaseJSONRenderer, BrowsableAPIRenderer]
