from django.urls import path
from . import views
from .views import DeleteUserView, CreateRequestView, GetRequestInfoView, GetImageView, GetUserHistoryView


class RegisterUserView:
    pass


class LoginUserView:
    pass


urlpatterns = [
    path('users', views.register, name='create_user'),
    path('users/get/<int:user_id>', views.get_user, name='get_user'),
    path('users/put/<int:user_id>', views.update_user, name='update_user'),
    path('users/delete/<int:user_id>', views.delete_user, name='delete_user'),
   # path('users/login/', LoginUserView.as_view()),
   # path('users/register/', RegisterUserView.as_view()),
    path('users/<int:user_id>/history/', GetUserHistoryView.as_view()),
    path('users/<int:user_id>/', DeleteUserView.as_view()),
    path('requests/', CreateRequestView.as_view()),
    path('requests/<int:request_id>/', GetRequestInfoView.as_view()),
    path('images/<int:image_id>/', GetImageView.as_view()),
]
