from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import *
from api.serializers import UserSerializer, UserSerializerWithToken

from django.views.decorators.csrf import csrf_exempt

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v
        return data
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['message'] = 'Welcome!'
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/<id>/',
        '/api/users/',
        '/api/users/profile/',
        '/api/users/login/',
        '/api/users/register/',
    ]
    return Response(routes)

@csrf_exempt
@api_view(['POST'])
def registerUser(request):
    data = request.data
    print("something is happening")
    try:
        # Debugging: Log incoming data
        print("Received request data:", data)

        # Attempt to create a user
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            password=make_password(data['password'])
        )

        # Debugging: Log user creation success
        print(f"User created successfully: {user.username}")

        # Serialize the user
        serializer = UserSerializerWithToken(user, many=False)

        # Debugging: Log the serialized response
        print("Serialized user data:", serializer.data)

        return Response(serializer.data)
    except Exception as e:
        # Debugging: Log any exception that occurs
        print("Error in registerUser view:", str(e))

        message = {'detail': 'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    serializer = UserSerializerWithToken(user, many=False)
    data = request.data
    user.first_name = data['name']
    user.username = data['email']
    if data['password'] != '':
        user.password = make_password(data['password'])
    user.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteUser(request, pk):
    userForDeletion = User.objects.get(id=pk)
    userForDeletion.delete()
    return Response('User was deleted')     
