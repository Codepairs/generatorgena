from rest_framework import serializers
from gena_database_app.models import User, ImageModel, UsageHistory



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
        fields = ['operationID', 'userID', 'imageID', 'prompt', 'createdAt', 'updatedAt', 'status']

    def create(self, validated_data):
        usage = UsageHistory.objects.create(
            userID=validated_data.get('userID', ''),
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
    



    
class GenaGenerateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    prompt = serializers.CharField(required=True)
    images = serializers.IntegerField(default=1, required=False)
    width = serializers.IntegerField(default=1024, required=False)
    height = serializers.IntegerField(default=1024, required=False)

    def validate_images(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество изображений должно быть не меньше 1.")
        return value

    def validate_width(self, value):
        if value <= 0:
            raise serializers.ValidationError("Ширина должна быть положительным числом.")
        return value

    def validate_height(self, value):
        if value <= 0:
            raise serializers.ValidationError("Высота должна быть положительным числом.")
        return value
