from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from .views import GetUserView, RegisterUserView, DeleteUserView, GetRequestView, GetImageView, \
    GetUserHistoryView, LogoutView, ChangePasswordView, GenerateImage

urlpatterns = [
    # сделано
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', RegisterUserView.as_view(), name='register'),
    # что бы это ни значило
    path('users/', DeleteUserView.as_view()),
    path('users/history/', GetUserHistoryView.as_view()),
    
    # сделано
    path('requests/', GenerateImage.as_view(), name='Generate'),
    # что бы это ни значило
    
    path('requests/<int:request_id>/', GetRequestView.as_view()),
    # сделано
    path('getimage/', GetImageView.as_view(), name='get-image'),
    # что бы это ни значило
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/change-password/', ChangePasswordView.as_view(), name='change_password')
]
