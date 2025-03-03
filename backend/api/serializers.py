from rest_framework import serializers
from .models import SystemUser, Announcement

class SystemUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = SystemUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff']
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)


    class Meta:
        model = SystemUser
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number']

    def validate_email(self, value):
        if SystemUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data):
        user = SystemUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', '')
        )
        return user
    
class AnnouncementSerializer(serializers.ModelSerializer):
    author = SystemUserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'subject', 'content', 'hourly_rate', 'author', 'date_added']