from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from gena_database_app.models import User, UsageHistory, ImageModel
from .serializers import UserSerializer,  ChangePasswordSerializer, UsageHistorySerializer, ImageModelSerializer, CustomTokenObtainPairSerializer
from django.conf import settings
import logging
import requests
import json
import time

import base64
from django.http import HttpResponse
from io import BytesIO
from PIL import Image


logger = logging.getLogger(__name__)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка регистрации пользователя: {str(e)}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)  # many=False, так как получаем одного пользователя
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetUserHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id, prompt_id):
        try:
            user = User.objects.get(id=user_id)
            history = UsageHistory.objects.filter(userID=user)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class GetRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id, operation_id):
        try:
            user = User.objects.get(id=user_id)
            history = UsageHistory.objects.filter(userID=user, operationID=operation_id)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Выход выполнен"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"message": "Пароль успешно изменён"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

###############
# Kandinsky api

class GetModelStatus(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
            }

            response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipelines', headers=AUTH_HEADERS)
            response.raise_for_status()  # Вызывает исключение, если статус ответа не 200
            data = response.json()
            pipeline_id = data[0]['id']
            return Response({'pipeline_id': pipeline_id})
        except requests.exceptions.RequestException as e:
            return Response({'error': 'Ошибка запроса'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except KeyError:
            return Response({'error': 'Нет ключа "id" в данных'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateImageGenerationRequest(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            data = request.data  # Получаем JSON-данные из тела запроса
            user_id = data.get("user_id")
            prompt = data.get("prompt")
            pipeline = data.get("pipeline")
            images = data.get("images", 1)
            width = data.get("width", 1024)
            height = data.get("height", 1024)

            if not user_id or not prompt or not pipeline:
                return Response({"error": "Не все обязательные параметры переданы"},
                                status=status.HTTP_400_BAD_REQUEST)
        
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

            if 'uuid' not in data:
                return Response({'error': 'Ответ API не содержит uuID', 'api_response': data},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            operation_info = {
                'userID': user_id,
                'modelPromptID': data['uuid'],
                'prompt': prompt,
                'status': 'created'
            }

            serializer = UsageHistorySerializer(data=operation_info)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except requests.exceptions.RequestException:
            return Response({'error': 'Ошибка при запросе к API'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class GetGeneratedImage(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            operation_id = request.query_params.get("operation_id")
            attempts = int(request.query_params.get("attempts", 10))
            delay = int(request.query_params.get("delay", 10))

            if not operation_id:
                return Response({"error": "Параметр 'operation_id' обязателен"}, status=status.HTTP_400_BAD_REQUEST)
            
            AUTH_HEADERS = {
            'X-Key': f'Key {settings.KANDINSKY_API_KEY}',
            'X-Secret': f'Secret {settings.KANDINSKY_SECRET_KEY}',
            }

            history = UsageHistory.objects.filter(operationID=operation_id).first()
            if not history:
                return Response({"error": "История с таким operation_id не найдена"}, status=status.HTTP_404_NOT_FOUND)
            
            request_id = history.modelPromptID
            while attempts > 0:
                response = requests.get('https://api-key.fusionbrain.ai/' + 'key/api/v1/pipeline/status/' + request_id, headers=AUTH_HEADERS)
                data = response.json()
                if data['status'] == 'DONE':
                    
                    if 'result' not in data:
                        return Response({'error': 'Ответ API не содержит результат', 'api_response': data},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    
                    image_info = {
                        'image_base64': data['result']['files'][0]
                    }

                    serializer = ImageModelSerializer(data=image_info)
                    if serializer.is_valid():
                        instance = serializer.save()
                        history.imageID = instance
                        history.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                attempts -= 1
                time.sleep(delay)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

###############

# получение изображения файлом
class GetImageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            image_id = request.query_params.get("image_id")
            image = ImageModel.objects.get(imageID=image_id)
            raw_image = image.image_base64
            
            # Декодируем base64
            image_data = base64.b64decode(raw_image)
            img = Image.open(BytesIO(image_data))
            
            # Сохраняем в поток в формате JPG
            img_io = BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            
            # Возвращаем файл пользователю
            response = HttpResponse(img_io, content_type='image/jpeg')
            response['Content-Disposition'] = f'attachment; filename="{image_id}.jpg"'
            return response
        except ImageModel.DoesNotExist:
            return Response({"message": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)