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
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['imageID', 'link_to_image', 'createdAt', 'rating']

    def create(self, validated_data):
        image = ImageModel.objects.create(
            link_to_image=validated_data.get('link_to_image', ''),
            rating=validated_data.get('rating', 0.0)
        )
        return image

    def update(self, instance, validated_data):
        instance.link_to_image = validated_data.get('link_to_image', instance.link_to_image)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance


class UsageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageHistory
        fields = ['operationID', 'uuID', 'userID', 'imageID', 'prompt', 'createdAt', 'updatedAt', 'status']

    def create(self, validated_data):
        usage = UsageHistory.objects.create(
            userID=validated_data.get('userID', ''),
            uuID=validated_data.get('uuID', ''),
            prompt=validated_data.get('prompt', ''),
            status='created',
            imageID=None
        )
        return usage

    def update(self, instance, validated_data):
        instance.prompt = validated_data.get('prompt', instance.prompt)
        instance.status = validated_data.get('status', instance.status)
        instance.imageID = validated_data.get('imageID', instance.imageID)
        instance.save()
        return instance