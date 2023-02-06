from django.urls import path

from status.api.views import (StatusAPIView, StaticAPIDetailView
                            # StatusDetailAPIView,
                            # StatusCreateAPIView,
                            # StatusUpdateAPIView,
                            # StatusDeleteAPIView
                            )

urlpatterns = [
    # path('', StatusListSearchAPIView.as_view()),
    path('', StatusAPIView.as_view()),
    path('<int:pk>', StaticAPIDetailView.as_view()),
    # path('create/', StatusCreateAPIView.as_view()),
    # path('<pk>/', StatusDetailAPIView.as_view()),
    # path('update/<pk>/', StatusUpdateAPIView.as_view()),
    # path('delete/<pk>/', StatusDeleteAPIView.as_view()),

]
