"""cfeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from updates.views import update_model_detail_view, JsonCBV, JsonCBV2,SerializedView, SerializedListView
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/status/', include('status.api.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name="token_obtain_pair"),
    path('api/auth/verifytoken/', TokenVerifyView.as_view(), name='token_verify'),

    # path('$/', update_model_detail_view, name=""),
    # path('jcvb/', JsonCBV.as_view()),
    # path('jcbv2/', JsonCBV2.as_view()),
    # path('sv/', SerializedView.as_view()),
    # path('slv/', SerializedListView.as_view()),
]
