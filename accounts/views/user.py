from accounts.models import User
from accounts.serializers import UserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class GetUser(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request) -> None:
        user = User.objects.filter(id=request.user.id).first()

        serializer = UserSerializer(user)

        return Response({
            "user": serializer.data,
        })