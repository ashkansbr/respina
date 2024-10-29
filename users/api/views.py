from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InputRegistrationSerializer, OutputRegistrationSerializer
from .services import create_user
from drf_spectacular.utils import extend_schema
from .selectors import get_users



class RegistrationApi(APIView):
    @extend_schema(request=InputRegistrationSerializer, responses=OutputRegistrationSerializer)
    def post(self, request):

        serializer = InputRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        try:
            query = create_user(email=serializer.validated_data.get('email'),
                                password=serializer.validated_data.get('password'))

        except Exception as e:
            return Response(f"database error{e}", status=status.HTTP_400_BAD_REQUEST)

        return Response(OutputRegistrationSerializer(query).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        users = get_users()
        if not users:
            return Response({"detail": "No users found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OutputRegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



