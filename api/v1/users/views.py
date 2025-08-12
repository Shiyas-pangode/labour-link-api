from rest_framework import generics ,status 
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny 
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import UserSerializer , LoginSerializer


class RegisterView(generics.CreateAPIView):
    
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({
                'status_code':6000,
                'message':'Succesfully registered',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        except ValidationError:
            return Response({
                'status_code': 6001,
                'message': 'User registration failed',
                'errors': serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'status_code':6002,
                'message':'An unexpected error occurred',
                'errors':str(e)
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'status_code': 6000,
                'message': 'Login successful',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'status_code': 6001,
            'message': 'Login failed',
            'errors': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'status_code': 6000,
                'message': "Logout successful"
            }, status=status.HTTP_200_OK)
        except KeyError:
            return Response({
                'status_code': 6002,
                'message': "Refresh token is required"
            }, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({
                'status_code': 6003,
                'message': "Invalid or expired token"
            }, status=status.HTTP_400_BAD_REQUEST)