from accounts.auth import Authentication
from accounts.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class SignIn(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = Authentication.signin(self, email=email, password=password)

        token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
            "refresh": str(token),
            "access": str(token.access_token)
        })