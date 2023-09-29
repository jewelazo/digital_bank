from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, UserSerializer
from .models import User
# Create your views here.

class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args,  **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user).data,
            "message": "User Created Successfully.  Now perform Login to get your token",   
        },status=status.HTTP_201_CREATED)
    