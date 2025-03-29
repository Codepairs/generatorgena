from rest_framework import serializers
from gena_database_app.models import User, ImageModel, UsageHistory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userID', 'email', 'password', 'userName']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # user = User.objects.create(**validated_data)
        user = User.objects.create(
            email=validated_data.get('email', ''),
            userName=validated_data.get('userName', ''),
            password=(validated_data['password'])
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.userName = validated_data.get('userName', instance.userName)
        if 'password' in validated_data:
            instance.password = (validated_data['password'])
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