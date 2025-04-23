from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from .serializers import RegisterSerializer, AnnouncementSerializer, SystemUserSerializer
from .models import Announcement, SystemUser
from .exceptions import (
    UserNotFoundException,
    AnnouncementNotFoundException,
    UnauthorizedAccessException,
    ValidationErrorException,
)
from django.db.models import Q


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationErrorException(detail=str(e))
    raise ValidationErrorException(detail=serializer.errors)


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
                raise ValidationErrorException(detail=f"Error during login: {str(e)}")
        raise ValidationErrorException(detail=serializer.errors)


@api_view(['GET'])
@permission_classes([AllowAny])
def announcement_list(request):
    announcements = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_announcement(request):
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationErrorException(detail=str(e))
    raise ValidationErrorException(detail=serializer.errors)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_announcement(request, pk):
    try:
        announcement = Announcement.objects.get(pk=pk)
        if request.user != announcement.author and not request.user.is_staff:
            raise UnauthorizedAccessException()
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise ValidationErrorException(detail=serializer.errors)
    except ObjectDoesNotExist:
        raise AnnouncementNotFoundException()
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    user = request.user
    serializer = SystemUserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        try:
            serializer.save()
            announcements = Announcement.objects.filter(author=user)
            for announcement in announcements:
                announcement.author = user
                announcement.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationErrorException(detail=f"Error updating user: {str(e)}")
    raise ValidationErrorException(detail=serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_announcement(request, pk):
    try:
        announcement = Announcement.objects.get(pk=pk)
        if request.user != announcement.author and not request.user.is_staff:
            raise UnauthorizedAccessException()
        announcement.delete()
        return Response({"message": "Announcement deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        raise AnnouncementNotFoundException()
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    try:
        user = request.user
        if not user:
            raise UserNotFoundException()
        serializer = SystemUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise ValidationErrorException(detail=f"Error fetching user: {str(e)}")

@api_view(['GET'])
@permission_classes([AllowAny])
def get_announcement(request, pk):
    try:
        announcement = Announcement.objects.get(pk=pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        raise AnnouncementNotFoundException()
    except Exception as e:
        raise ValidationErrorException(detail=f"Error fetching announcement: {str(e)}")
    

@api_view(['GET'])
@permission_classes([AllowAny])
def search_announcements(request):
    subject = request.query_params.get('subject', None)
    min_rate = request.query_params.get('min_rate', None)
    max_rate = request.query_params.get('max_rate', None)

    try:
        announcements = Announcement.objects.all()

        if subject:
            announcements = announcements.filter(subject__icontains=subject)
        if min_rate:
            announcements = announcements.filter(hourly_rate__gte=min_rate)
        if max_rate:
            announcements = announcements.filter(hourly_rate__lte=max_rate)

        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise ValidationErrorException(detail=f"Error searching announcements: {str(e)}")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    if not request.user.is_staff:
        raise UnauthorizedAccessException()
    users = SystemUser.objects.all()
    serializer = SystemUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    if not request.user.is_staff:
        raise UnauthorizedAccessException()
    try:
        user = SystemUser.objects.get(pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        raise UserNotFoundException()