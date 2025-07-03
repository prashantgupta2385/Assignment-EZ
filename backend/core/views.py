from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer
from .models import User
from django.urls import reverse
from django.conf import settings
import jwt

SECRET_KEY = settings.SECRET_KEY


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create JWT token for email verification
        token = jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm='HS256')

        # Build full verification URL
        verify_url = request.build_absolute_uri(reverse('verify-email')) + f"?token={token}"

        return Response({
            "message": "Registration successful. Use the verification URL to activate your account.",
            "verify_url": verify_url
        }, status=status.HTTP_201_CREATED)


class VerifyEmailView(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if user.is_verified:
                return Response({"message": "Account already verified."}, status=200)

            user.is_verified = True
            user.is_active = True
            user.save()
            return Response({"message": "Email verified successfully."}, status=200)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=400)
        except jwt.DecodeError:
            return Response({"error": "Invalid token"}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
