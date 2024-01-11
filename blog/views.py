from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing post instances.
    - list: Get all posts
    - create: Create a new post
    - retrieve: Get a specific post
    - update: Update a specific post
    - partial_update: Partially update a specific post
    - destroy: Delete a specific post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """
        Custom action to change the status of a post to 'published'.
        """
        post = self.get_object()
        post.status = 'published'
        post.save()
        return Response({'status': 'post published'}, status=status.HTTP_200_OK)

    @action(detail=False)
    def drafts(self, request):
        """
        Custom action to list all draft posts for the logged-in user.
        """
        drafts = Post.objects.filter(author=request.user, status='draft')
        serializer = self.get_serializer(drafts, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def user_posts(self, request):
        """
        Custom action to list all posts by a specific user.
        """
        username = request.query_params.get('username', None)
        posts = Post.objects.filter(author__username=username) if username else Post.objects.none()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def search(self, request):
        """
        Custom action to search posts based on a query.
        """
        query = request.query_params.get('query', None)
        posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query) if query else Post.objects.none()
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
