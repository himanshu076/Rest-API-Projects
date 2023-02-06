from rest_framework import viewsets
from rest_framework.views import APIView
from blog_app.serializers import PostSerializer, UpvoteSerializer, CommentSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from blog_app.models import Post, Upvote, Comment
from blog_app.permission import IsOwnerOrReadOnly
from accounts.models import User


# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'body': request.data.get('body')
        }
        serializer = PostSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        #breakpoint()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UpvoteViewSet(viewsets.ModelViewSet):
    #queryset = Post.objects.all()
    serializer_class = PostSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        post = self.object(pk)
        if post is None:
            return None

        upvoters = post.upvotes.all().values_list('user', flat = True)
        if self.request.user.id in upvoters:
            post.upvote_count -= 1
            post.upvotes.filter(user = self.request.user).delete()
        else:
            post.upvote_count += 1
            upvote = Upvote(user = self.request.user, post = post)
            upvote.save()
        post.save()
        queryset = Post.objects.all()
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    #queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            #breakpoint()
            return None

    def comment(self, pk):
        #breakpoint()
        try:
            return Comment.objects.get(pk = pk)
        except Comment.DoesNotExist:
            return None

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs['pk']
        post = self.object(pk)
        if post is None:
            return None
        queryset = Comment.objects.filter(post = post).all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk_2']
        comment = self.comment(pk)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        #breakpoint()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'post': kwargs['pk'],
            'body': request.data.get('body')
        }
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs['pk_2']
        comment = self.comment(pk)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(comment, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(comment, '_prefetched_objects_cache', None):
            comment._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk_2']
        comment = self.comment(pk)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(comment)
        return Response(status=status.HTTP_204_NO_CONTENT)

        '''
class PostListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'body': request.data.get('body')
        }
        serializer = PostSerializer(data = data)
        breakpoint()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'title': request.data.get('title'),
            'body': request.data.get('body'),
            'upvote_count': post.upvote_count
        }
        serializer = PostSerializer(post, data = data, partial = True)
        if serializer.is_valid():
            if post.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status = status.HTTP_200_OK)
            return Response({"error": "You are not authorized to edit this post"}, status = status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        if post.user.id == request.user.id:
            post.delete()
            return Response({"res": "Object deleted!"}, status = status.HTTP_200_OK)
        return Response({"error": "You are not authorized to delete this post"}, status = status.HTTP_401_UNAUTHORIZED)


class UserPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        user = User.objects.filter(username = username).first()
        if user is None:
            return Response({'error': 'User not found'}, status = status.HTTP_404_NOT_FOUND)
        posts = Post.objects.filter(user = user)
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)


class UpvoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)

        upvoters = post.upvotes.all().values_list('user', flat = True)
        if request.user.id in upvoters:
            post.upvote_count -= 1
            post.upvotes.filter(user = request.user).delete()
        else:
            post.upvote_count += 1
            upvote = Upvote(user = request.user, post = post)
            upvote.save()
        post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data, status = status.HTTP_200_OK)


class CommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk = pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        comments = Comment.objects.filter(post = post)
        serializer = CommentSerializer(comments, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)

    def post(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response({'error': 'Post not found'}, status = status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user.id,
            'post': post.id,
            'body': request.data.get('body')
        }
        serializer = CommentSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

'''