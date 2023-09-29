from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


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


class LogoutApi(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data.get("username"))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({"response": "Success Logout"},status=status.HTTP_200_OK)
        return Response({"response": "Doesn't exist user with that username"},status=status.HTTP_400_BAD_REQUEST)
