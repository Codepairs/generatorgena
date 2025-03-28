from django.urls import path
from .views import GetUserView, RegisterUserView, DeleteUserView, CreateUsageView, GetRequestView, GetImageView, GetUserHistoryView



urlpatterns = [
    path('users/login/', GetUserView.as_view()),
    path('users/register/', RegisterUserView.as_view()),
    path('users/<int:user_id>', DeleteUserView.as_view()),
    path('users/<int:user_id>/history/', GetUserHistoryView.as_view()),
    path('users/<int:user_id>/', DeleteUserView.as_view()),
    path('requests/', CreateUsageView.as_view()),
    path('requests/<int:request_id>/', GetRequestView.as_view()),
    path('images/<int:image_id>/', GetImageView.as_view()),
]
