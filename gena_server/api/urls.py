from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import GetUserView, RegisterUserView, DeleteUserView, GetRequestView, GetImageView, \
    GetUserHistoryView, LogoutView, ChangePasswordView, GenerateImage

urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', RegisterUserView.as_view(), name='register'),
    path('users/<int:user_id>', DeleteUserView.as_view()),
    path('users/history/', GetUserHistoryView.as_view()),
    path('users/<int:user_id>/', DeleteUserView.as_view()),
    path('requests/', GenerateImage.as_view(), name='Generate'),
    path('requests/<int:request_id>/', GetRequestView.as_view()),
    path('getimage/', GetImageView.as_view(), name='get-image'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change_password')
]
