from rest_framework import serializers
from gena_database_app.models import User, Request, ImageModel, UsageHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'email', 'password', 'userName']  # Include password for creation only
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Hash password before creating user in real scenario
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        # Hash password if it's updated
        instance.email = validated_data.get('email', instance.email)
        instance.userName = validated_data.get('userName', instance.userName)
        if 'password' in validated_data:
            instance.password = validated_data['password']  # Hash this in real application
        instance.save()
        return instance


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'text_description', 'user', 'status']

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['imageID', 'link_to_image', 'createdAt', 'rating']

class UsageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageHistory
        fields = ['operationID', 'userID', 'imageID', 'prompt', 'createdAt', 'updatedAt', 'status']

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id', 'text_description', 'user', 'status']