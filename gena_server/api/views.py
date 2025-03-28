from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from gena_database_app.models import User, UsageHistory, ImageModel
from .serializers import UserSerializer, UsageHistorySerializer, ImageModelSerializer
from django.conf import settings
import logging
import requests
import json
import time

logger = logging.getLogger(__name__)



class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(userID=user_id)
            serializer = UserSerializer(user)  # many=False, так как получаем одного пользователя
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserView(APIView):
    def put(self, request, user_id):
        try:
            user = User.objects.get(userID=int(user_id))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(userID=int(user_id))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetUserHistoryView(APIView):
    def get(self, request, user_id, prompt_id):
        try:
            user = User.objects.get(userID=user_id)
            history = UsageHistory.objects.filter(userID=user)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class GetRequestView(APIView):
    def get(self, request, user_id, prompt_id):
        try:
            user = User.objects.get(userID=user_id)
            history = UsageHistory.objects.filter(userID=user, operationID=prompt_id)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class CreateUsageView(CreateAPIView):
    serializer_class = UsageHistorySerializer

###############
# Kandinsky api

class GetModelStatus(APIView):
    def get(self):
        AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
        }
        response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipelines', headers=AUTH_HEADERS)
        data = response.json()
        pipeline_id = data[0]['id']
        return pipeline_id

class CreateImageGenerationRequest(APIView):
    def post(self, prompt, pipeline, images=1, width=1024, height=1024):
        AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
        }
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": "{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipeline/run', headers=AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']
    
class GetGeneratedImage(APIView):
    def get(self, request_id, attempts=10, delay=10):
        AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
        }
        while attempts > 0:
            response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipeline/status/' + request_id, headers=AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['files']

            attempts -= 1
            time.sleep(delay)

###############


class GetImageView(APIView):
    def get(self, request, image_id):
        try:
            image = ImageModel.objects.get(imageID=image_id)
            serializer = ImageModelSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ImageModel.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)