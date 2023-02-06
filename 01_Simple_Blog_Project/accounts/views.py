from rest_framework import viewsets
from accounts.models import User
from accounts.serializers import UserModelSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    #authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

