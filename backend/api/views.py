from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, AnnouncementSerializer, SystemUserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Announcement


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        print("Request data:", request.data)  # Debug print
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error saving user:", str(e))  # Debug print
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Serializer errors:", serializer.errors)  # Debug print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = TokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                user = serializer.user
                response_data = {
                    'refresh': validated_data['refresh'],
                    'access': validated_data['access'],
                    'user_id': user.id
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                print("Error during login:", str(e))  # Debug print
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Serializer errors:", serializer.errors)  # Debug print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def announcement_list(request):
    if request.method == 'GET':
        try:
            announcements = Announcement.objects.all()
            serializer = AnnouncementSerializer(announcements, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching announcements:", str(e))  # Debug print
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_announcement(request):
    if request.method == 'POST':
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Error saving announcement:", str(e))  # Debug print
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Serializer errors:", serializer.errors)  # Debug print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user == announcement.author or request.user.is_staff:
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as e:
                print("Error updating announcement:", str(e))  # Debug print
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Serializer errors:", serializer.errors)  # Debug print
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You do not have permission to edit this announcement.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    user = request.user
    serializer = SystemUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            # Update announcements authored by the user
            announcements = Announcement.objects.filter(author=user)
            for announcement in announcements:
                announcement.author = user
                announcement.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error updating user:", str(e))  # Debug print
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    print("Serializer errors:", serializer.errors)  # Debug print
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_announcement(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    if request.user == announcement.author or request.user.is_staff:
        try:
            announcement.delete()
            return Response({'message': 'Announcement deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("Error deleting announcement:", str(e))  # Debug print
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'error': 'You do not have permission to delete this announcement.'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    serializer = SystemUserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_announcement(request, pk):
    try:
        announcement = get_object_or_404(Announcement, pk=pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print("Error fetching announcement:", str(e))  # Debug print
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)