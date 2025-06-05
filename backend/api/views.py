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
from .tasks import send_notification
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(method='post', request_body=RegisterSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Register a new user.

    ---
    parameters:
      - name: username
        description: Username for the new user
        required: true
        type: string
      - name: email
        description: Email address of the user
        required: true
        type: string
      - name: password
        description: Password for the user
        required: true
        type: string
      - name: first_name
        description: First name of the user
        required: true
        type: string
      - name: last_name
        description: Last name of the user
        required: true
        type: string
      - name: phone_number
        description: Phone number of the user (optional)
        required: false
        type: string
    responses:
      201:
        description: User created successfully
      400:
        description: Validation error
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
          user = serializer.save()
          send_notification.delay(user.email, "Welcome to our service!")
          return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            if hasattr(e, 'detail'):
                raise ValidationErrorException(detail=e.detail)
            raise ValidationErrorException(detail=str(e))
    print("Serializer errors:", serializer.errors) 
    raise ValidationErrorException(detail=serializer.errors)

@swagger_auto_schema(
    method='post',
    request_body=TokenObtainPairSerializer,
    responses={
        200: openapi.Response(
            description="Authentication successful",
            examples={
                "application/json": {
                    "refresh": "string",
                    "access": "string",
                    "user_id": 1
                }
            }
        ),
        400: "Invalid credentials"
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate a user and return JWT tokens.

    ---
    parameters:
      - name: username
        description: Username of the user
        required: true
        type: string
      - name: password
        description: Password of the user
        required: true
        type: string
    responses:
      200:
        description: Authentication successful
        schema:
          type: object
          properties:
            refresh:
              type: string
              description: Refresh token
            access:
              type: string
              description: Access token
            user_id:
              type: integer
              description: ID of the authenticated user
      400:
        description: Invalid credentials
    """
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
    """
    Retrieve a list of all announcements.

    ---
    responses:
      200:
        description: A list of announcements
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID of the announcement
              subject:
                type: string
                description: Subject of the announcement
              content:
                type: string
                description: Content of the announcement
              hourly_rate:
                type: number
                format: float
                description: Hourly rate for the announcement
              author:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID of the author
                  first_name:
                    type: string
                    description: First name of the author
                  last_name:
                    type: string
                    description: Last name of the author
    """
    paginator = PageNumberPagination()
    paginator.page_size = 10  # or remove to use global PAGE_SIZE
    announcements = Announcement.objects.all().order_by('-date_added')
    result_page = paginator.paginate_queryset(announcements, request)
    serializer = AnnouncementSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
    
    
@swagger_auto_schema(
    method='post',
    request_body=TokenObtainPairSerializer,
    responses={
        200: openapi.Response(
            description="Authentication successful",
            examples={
                "application/json": {
                    "refresh": "string",
                    "access": "string",
                    "user_id": 1
                }
            }
        ),
        400: "Invalid credentials"
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_announcement(request):
    """
    Add a new announcement.

    ---
    parameters:
      - name: subject
        description: Subject of the announcement
        required: true
        type: string
      - name: content
        description: Content of the announcement
        required: true
        type: string
      - name: hourly_rate
        description: Hourly rate for the announcement
        required: true
        type: number
        format: float
    responses:
      201:
        description: Announcement created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the announcement
            subject:
              type: string
              description: Subject of the announcement
            content:
              type: string
              description: Content of the announcement
            hourly_rate:
              type: number
              format: float
              description: Hourly rate for the announcement
            author:
              type: object
              properties:
                id:
                  type: integer
                  description: ID of the author
                first_name:
                  type: string
                  description: First name of the author
                last_name:
                  type: string
                  description: Last name of the author
      400:
        description: Validation error
    """
    serializer = AnnouncementSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            raise ValidationErrorException(detail=str(e))
    raise ValidationErrorException(detail=serializer.errors)


@swagger_auto_schema(
    method='put',
    request_body=AnnouncementSerializer,
    responses={
        200: AnnouncementSerializer,
        400: "Validation error",
        403: "Unauthorized access",
        404: "Announcement not found"
    }
)    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_announcement(request, pk):
    """
    Edit an existing announcement.

    ---
    parameters:
      - name: id
        description: ID of the announcement to edit
        required: true
        type: integer
      - name: subject
        description: New subject of the announcement (optional)
        required: false
        type: string
      - name: content
        description: New content of the announcement (optional)
        required: false
        type: string
      - name: hourly_rate
        description: New hourly rate for the announcement (optional)
        required: false
        type: number
        format: float
    responses:
      200:
        description: Announcement updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the announcement
            subject:
              type: string
              description: Updated subject of the announcement
            content:
              type: string
              description: Updated content of the announcement
            hourly_rate:
              type: number
              format: float
              description: Updated hourly rate for the announcement
      403:
        description: Unauthorized access
      404:
        description: Announcement not found
      400:
        description: Validation error
    """
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


@swagger_auto_schema(
    method='put',
    request_body=SystemUserSerializer,
    responses={
        200: SystemUserSerializer,
        400: "Validation error"
    }
)    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_user(request):
    """
    Edit the current user's profile.

    ---
    parameters:
      - name: first_name
        description: New first name of the user (optional)
        required: false
        type: string
      - name: last_name
        description: New last name of the user (optional)
        required: false
        type: string
      - name: email
        description: New email address of the user (optional)
        required: false
        type: string
      - name: phone_number
        description: New phone number of the user (optional)
        required: false
        type: string
    responses:
      200:
        description: User profile updated successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the user
            first_name:
              type: string
              description: Updated first name of the user
            last_name:
              type: string
              description: Updated last name of the user
            email:
              type: string
              description: Updated email address of the user
            phone_number:
              type: string
              description: Updated phone number of the user
      400:
        description: Validation error
    """
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


@swagger_auto_schema(
    method='delete',
    manual_parameters=[
        openapi.Parameter('id', openapi.IN_PATH, description="ID of the announcement to delete", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: "Announcement deleted successfully",
        403: "Unauthorized access",
        404: "Announcement not found"
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_announcement(request, pk):
    """
    Delete an announcement.

    ---
    parameters:
      - name: id
        description: ID of the announcement to delete
        required: true
        type: integer
    responses:
      204:
        description: Announcement deleted successfully
      403:
        description: Unauthorized access
      404:
        description: Announcement not found
    """
    try:
        announcement = Announcement.objects.get(pk=pk)
        if request.user != announcement.author and not request.user.is_staff:
            raise UnauthorizedAccessException()
        announcement.delete()
        return Response({"message": "Announcement deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        raise AnnouncementNotFoundException()
    

@swagger_auto_schema(
    method='get',
    responses={200: SystemUserSerializer}
)    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Retrieve the current user's profile.

    ---
    responses:
      200:
        description: User profile retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              description: ID of the user
            first_name:
              type: string
              description: First name of the user
            last_name:
              type: string
              description: Last name of the user
            email:
              type: string
              description: Email address of the user
            phone_number:
              type: string
              description: Phone number of the user
            is_staff:
              type: boolean
              description: Whether the user is an admin
    """
    try:
        user = request.user
        if not user:
            raise UserNotFoundException()
        serializer = SystemUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        raise ValidationErrorException(detail=f"Error fetching user: {str(e)}")


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="ID of the announcement", type=openapi.TYPE_INTEGER)
    ],
    responses={200: AnnouncementSerializer, 404: "Announcement not found"}
)
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
    

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('subject', openapi.IN_QUERY, description="Subject filter", type=openapi.TYPE_STRING),
        openapi.Parameter('min_rate', openapi.IN_QUERY, description="Minimal rate", type=openapi.TYPE_NUMBER),
        openapi.Parameter('max_rate', openapi.IN_QUERY, description="Maximal rate", type=openapi.TYPE_NUMBER),
    ],
    responses={200: AnnouncementSerializer(many=True)}
)
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


@swagger_auto_schema(
    method='get',
    responses={200: SystemUserSerializer(many=True), 403: "Unauthorized access"}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list(request):
    """
    Retrieve a list of all users (admin only).

    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: ID of the user
              first_name:
                type: string
                description: First name of the user
              last_name:
                type: string
                description: Last name of the user
              email:
                type: string
                description: Email address of the user
              phone_number:
                type: string
                description: Phone number of the user
              is_staff:
                type: boolean
                description: Whether the user is an admin
      403:
        description: Unauthorized access
    """
    if not request.user.is_staff:
        raise UnauthorizedAccessException()
    users = SystemUser.objects.all()
    serializer = SystemUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='delete',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="ID of the user to delete", type=openapi.TYPE_INTEGER)
    ],
    responses={
        204: "User deleted successfully",
        403: "Unauthorized access",
        404: "User not found"
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    """
    Delete a user (admin only).

    ---
    parameters:
      - name: id
        description: ID of the user to delete
        required: true
        type: integer
    responses:
      204:
        description: User deleted successfully
      403:
        description: Unauthorized access
      404:
        description: User not found
    """
    if not request.user.is_staff:
        raise UnauthorizedAccessException()
    try:
        user = SystemUser.objects.get(pk=pk)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        raise UserNotFoundException()