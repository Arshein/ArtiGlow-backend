from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Post
from posts.serializer import PostSerializer

from rest_framework import filters


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['description']

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_superuser:
            return Post.objects.all()
        else:
            request_type = self.request.method
            if request_type == 'DELETE':
                return Post.objects.filter(owner=user)
            elif request_type == "GET":
                return Post.objects.all()
            else:
                return Post.objects.none

