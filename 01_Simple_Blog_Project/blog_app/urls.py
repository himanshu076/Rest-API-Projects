from django.urls import path
from blog_app.views import PostViewSet, UpvoteViewSet, CommentViewSet
#from blog_app.views import PostListAPIView, PostDetailAPIView, UserPostAPIView, UpvoteAPIView, CommentAPIView


post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

upvote_post = UpvoteViewSet.as_view({
    'get': 'retrieve',
})

comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
comment_list_post_related = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


urlpatterns = [
    path('post', post_list),
    path('post/<int:pk>', post_detail),
    path('post/<int:pk>/upvote', upvote_post, name='post_detail'),
    path('post/<int:pk>/comment/<int:pk_2>', comment_detail),
    path('post/<int:pk>/comment', comment_list_post_related),
]
'''

urlpatterns = [
    path('', PostListAPIView.as_view()),
    path('<int:pk>/', PostDetailAPIView.as_view()),
    path('<int:pk>/upvote/', UpvoteAPIView.as_view()),
    path('<int:pk>/comment/', CommentAPIView.as_view()),
    path('<username>/', UserPostAPIView.as_view())
]
'''