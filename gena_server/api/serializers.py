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
                userName=validated_data.get('userName', '')
            )
        user.set_password(validated_data['password'])
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

class UsageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageHistory
        fields = ['operationID', 'userID', 'imageID', 'prompt', 'createdAt', 'updatedAt', 'status']

