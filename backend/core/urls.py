from django.urls import path
from .views import RegisterView, VerifyEmailView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path('login/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
]
