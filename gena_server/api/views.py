from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from gena_database_app.models import User, UsageHistory, Request, ImageModel
from .serializers import UserSerializer, UsageHistorySerializer, RequestSerializer, ImageModelSerializer
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user(request, user_id):
    try:
        user = User.objects.get(userID=int(user_id))
    except User.DoesNotExist:
        logger.error(f"User with ID {user_id} not found.")

        return Response(data={"error": "User not found", "user_id": int(user_id)}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)
@api_view(['PUT'])
def update_user(request, user_id):
    try:
        user = User.objects.get(userID=int(user_id))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(userID=int(user_id))
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class GetUserHistoryView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(userID=user_id)
            history = UsageHistory.objects.filter(userID=user)
            serializer = UsageHistorySerializer(history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteUserView(DestroyAPIView):
    queryset = User.objects.all()

class CreateRequestView(CreateAPIView):
    serializer_class = RequestSerializer

class GetRequestInfoView(RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

class GetImageView(APIView):
    def get(self, request, image_id):
        try:
            image = ImageModel.objects.get(imageID=image_id)
            serializer = ImageModelSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ImageModel.DoesNotExist:
            return Response({"message": "Image not found"}, status=status.HTTP_404_NOT_FOUND)