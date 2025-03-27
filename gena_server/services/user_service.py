import uuid

from gena_database_app.models import User


class user_service:
    def create_user(self, email, password, usrname):
        try:
            user = User.objects.create(userID = uuid.uuid4(), email=email, password=password, userName=username)
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    def get_user(self, user_id):
        try:
            user = User.objects(userID = user_id)
            return user
        except Exception as e:
            print(f"Error with finding an user: {e}")
            return None

    def delete_user(self, user_id):
        try:
            user = User.objects(userID=user_id)
            user.delete()
            return user
        except Exception as e:
            print(f"Error with delete an user: {e}")
            return None

    def update_user(self, user_id, email=None, password=None, username=None):
        try:
            user = User.objects(userID = user_id)
            user.userName = username
            user.email = email
            user.password = password
            return user
        except Exception as e:
            print(f"Error with update an user: {e}")
            return None