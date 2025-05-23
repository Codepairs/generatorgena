from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from gena_database_app.models import User, UsageHistory, ImageModel
from .serializers import UserSerializer,  ChangePasswordSerializer, UsageHistorySerializer, ImageModelSerializer, \
                         GenaGenerateSerializer

from django.conf import settings
import logging
import requests

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
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)  # many=False, так как получаем одного пользователя
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
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
    def delete(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GetUserHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user_id = request.query_params.get('user_id')
            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=user_id)
            history = UsageHistory.objects.filter(userID=user)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class GetRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, request_id):
        try:
            user_id = request.query_params.get('user_id')
            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(id=user_id)
            operation_id = request.data.get("operation_id")
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
    

###############
###############
# Kandinsky api
        
#class GenerateImage(APIView):
#    permission_classes = [IsAuthenticated]
#    def post(self, request):
#        #user_id
#        #prompt
#        try:
#            serializer = FusionBrainSerializer(data=request.data)
#            serializer.is_valid(raise_exception=True)
#            client = serializer.save()
#            pipeline_id = client.get_pipeline()
#        except requests.exceptions.RequestException as e:
#            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#        
#        try:
#            generate_serializer = GenerateSerializer(data=request.data)
#            generate_serializer.is_valid(raise_exception=True)
#            data = generate_serializer.validated_data   
#
#            if request.user.id != data['user_id']:
#                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
#
#            uuid = client.generate(prompt=data['prompt'], pipeline=pipeline_id)
#
#            operation_info = {
#                'userID': data['user_id'],
#                'prompt': data['prompt'],
#                'status': 'created'
#            }
#
#            history_serializer = UsageHistorySerializer(data=operation_info)
#            history_serializer.is_valid(raise_exception=True)
#            history_instance = history_serializer.save()
#        except requests.exceptions.RequestException:
#            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#        try:
#            result = client.check_generation(request_id=uuid)

#            image_info = {
#                'image_base64': result[0]
#            }
#            imgae_serializer = ImageModelSerializer(data=image_info)
#            imgae_serializer.is_valid(raise_exception=True)
#            image_instance = imgae_serializer.save()
#
#           history_instance.imageID = image_instance
#            history_instance.status = 'generated'
#            history_instance.save()
#
#            response_serializer = UsageHistorySerializer(history_instance)
#
#            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#        except requests.exceptions.RequestException:
#            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
############### GENA

class GenerateImage(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        #user_id
        #prompt
        
        #try:
        #    serializer = GenaSerializer(data=request.data)
        #    serializer.is_valid(raise_exception=True)
        #    client = serializer.save()
        #except requests.exceptions.RequestException as e:
        #    return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            generate_serializer = GenaGenerateSerializer(data=request.data)
            generate_serializer.is_valid(raise_exception=True)
            data = generate_serializer.validated_data   

            if request.user.id != data['user_id']:
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)

            response = requests.post(
                "http://ml_service:5000/generate/",
                json={"prompt": data['prompt']}
            )
            if response.status_code != 200:
                return Response({'error': 'Ошибка генерации'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result = response.json()["images"]

            operation_info = {
                'userID': data['user_id'],
                'prompt': data['prompt'],
                'status': 'created'
            }

            history_serializer = UsageHistorySerializer(data=operation_info)
            history_serializer.is_valid(raise_exception=True)
            history_instance = history_serializer.save()
        except requests.exceptions.RequestException:
            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        try:
            image_info = {
                'image_base64': result[0]
            }
            imgae_serializer = ImageModelSerializer(data=image_info)
            imgae_serializer.is_valid(raise_exception=True)
            image_instance = imgae_serializer.save()

            history_instance.imageID = image_instance
            history_instance.status = 'generated'
            history_instance.save()

            response_serializer = UsageHistorySerializer(history_instance)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except requests.exceptions.RequestException:
            return Response({'error': 'Ошибка сервера'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



###############

# получение изображения файлом
class GetImageView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            operation_id = request.query_params.get("operation_id")
            user_id = request.query_params.get("user_id")

            if request.user.id != int(user_id):
                return Response({"message": "Доступ к данным другого пользователя запрещен"}, status=status.HTTP_403_FORBIDDEN)
            operation = UsageHistory.objects.get(operationID=operation_id, userID = user_id)
            image = operation.imageID
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
            response['Content-Disposition'] = f'attachment; filename="{image.imageID}.jpg"'
            return response
        except ImageModel.DoesNotExist:
            return Response({"message": "Изображение не найдено"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)