from rest_framework import serializers
from gena_database_app.models import User, ImageModel, UsageHistory
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



#class UserSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ['userID', 'email', 'password', 'userName']
#        extra_kwargs = {'password': {'write_only': True}}

#    def create(self, validated_data):
        # user = User.objects.create(**validated_data)
#        user = User.objects.create(
#            email=validated_data.get('email', ''),
#            userName=validated_data.get('userName', ''),
#        )
#        user.set_password(validated_data.get('password', ''))
#        return user

#    def update(self, instance, validated_data):
#        instance.email = validated_data.get('email', instance.email)
#        instance.userName = validated_data.get('userName', instance.userName)
#        if 'password' in validated_data:
#            instance.set_password(validated_data.get('password', ''))
#        instance.save()
#        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))
        return super().update(instance, validated_data)



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Старый пароль неверен.")
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для входа по email вместо username"""
    username_field = 'email'
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email  # Добавляем email в токен
        return token

    def validate(self, attrs):
        """Изменяем логику валидации, чтобы использовать email вместо username"""
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        # этот метод при попыте получения токена выдаёт ошибку
        if not user.check_password(password):
            raise serializers.ValidationError("Неверный пароль.")

        # Создаем токен без вызова super()
        data = {}
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['imageID', 'image_base64', 'createdAt', 'rating']

    def create(self, validated_data):
        image = ImageModel.objects.create(
            image_base64=validated_data.get('image_base64', ''),
            rating=validated_data.get('rating', 0.0)
        )
        return image

    def update(self, instance, validated_data):
        instance.image_base64 = validated_data.get('image_base64', instance.image_base64)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class UsageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageHistory
        fields = ['operationID', 'modelPromptID', 'userID', 'imageID', 'prompt', 'createdAt', 'updatedAt', 'status']

    def create(self, validated_data):
        usage = UsageHistory.objects.create(
            userID=validated_data.get('userID', ''),
            modelPromptID=validated_data.get('modelPromptID', ''),
            prompt=validated_data.get('prompt', ''),
            status=validated_data.get('status', 'created'),
            imageID=None
        )
        return usage

    def update(self, instance, validated_data):
        instance.prompt = validated_data.get('prompt', instance.prompt)
        instance.status = validated_data.get('status', instance.status)
        instance.imageID = validated_data.get('imageID', instance.imageID)
        instance.save()
        return instance