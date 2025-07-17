
from django.contrib.auth import  get_user_model
from rest_framework import  serializers
import os 
import cloudinary
import cloudinary.uploader  
from django.core.cache import cache
from google.oauth2 import id_token as google_id_token
from rest_framework_simplejwt.tokens import RefreshToken
from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from  google.auth.transport import requests
from django.conf import settings



User=get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    # role=serializers.CharField(required=False)
    otp= serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model=User
        fields=['username','password','email','otp']
    def validate(self, data):
        email = data.get('email')
        input_otp = data.get('otp')
        key = f"otp:register:{email}"
        stored_otp = cache.get(key)

        if not stored_otp or stored_otp != input_otp:
            raise serializers.ValidationError("Invalid or expired OTP.")

        # OTP is valid, delete it to prevent reuse
        cache.delete(key)
        return data

    


    def create(self,validated_data):
        validated_data.pop('otp', None)  # Remove otp if it exists, as it's not needed for user creation
        return User.objects.create_user(**validated_data)


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # otp= serializers.CharField(write_only=True, required=False, allow_blank=True)
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
      

        return token
    
    def validate(self, attrs):
        login_value = attrs.get('email')  # using username key to accept either username or email
        password = attrs.get('password')
        otp=attrs.get("otp")

        try:
            # Check if it's an email or username
            if '@' in login_value:
                user = User.objects.get(email=login_value)
            else:
                print("username",login_value)
                user = User.objects.get(username=login_value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user doesnt exist")
    
        
        
        if cache.get(f"otp:login:{user.email}") != otp:
            raise serializers.ValidationError("Invalid or expired OTP.")    
         
        if not user.check_password(password):
            raise serializers.ValidationError("password is incorrect")
        cache.delete(f"otp:login:{user.email}")

        # Inject the actual username into attrs for token creation
        attrs['username'] = user.username
        self.user = user

        # Let super() generate the token using username
        data = super().validate(attrs)

        # Add custom claims
        data['username'] = user.username
        data['email'] = user.email

        return data


print(settings.GOOGLE_CLIENT_ID)
class LoginGoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(required=True)

    def validate(self, attrs):
        id_token_value = attrs.get('id_token')

        try:
            # Verify the token with Google's servers
            id_info = google_id_token.verify_oauth2_token(
                id_token_value,
                requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )
            print(settings.GOOGLE_CLIENT_ID)

            email = id_info.get('email')

            # Try to find existing user, or create with blank username
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': None}  # intentionally skipping username
            )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            print('verified google token')
            return {
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
                'username': user.username,
                'email': user.email,
                'is_new_user': created
            }

        except ValueError:
            raise serializers.ValidationError("Invalid Google ID token.")
        except Exception as e:
            raise serializers.ValidationError(str(e))

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError("Old password is incorrect")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp= serializers.CharField(write_only=True, required=True, allow_blank=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        # Check if the user exists
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "User with this email does not exist."})
        print('ver')
        if not cache.get(f"otp:forget:{email}") == otp:
            raise serializers.ValidationError({"otp": "Invalid or expired OTP."})
        cache.delete(f"otp:forget:{email}")  # Delete OTP after validation
        print('otp verified')
        return data
    
    
    def save(self, **kwargs):
        email = self.validated_data['email']
        new_password = self.validated_data['new_password']
        
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        
        return user

      
class UsernameCheckSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

from rest_framework import serializers
from cloudinary.uploader import upload as cloudinary_upload
from .models import User  # Adjust path as needed


class ProfileSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(required=False, write_only=True)
    
    linkedin = serializers.URLField(required=False, allow_blank=True)
    github = serializers.URLField(required=False, allow_blank=True)
    twitter = serializers.URLField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'name', 'username', 'role', 'bio', 'photo',
            'linkedin', 'github', 'twitter', 'website'
        ]



    def update(self, instance, validated_data):
    # Handle new image upload
        new_image = validated_data.pop('photo', None)
        old_image_url = instance.profile  # Save old image URL for later deletion
        uploaded = None

        if new_image:
            if not new_image.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise serializers.ValidationError("Image must be a PNG, JPG, or JPEG file.")
            uploaded = cloudinary_upload(new_image)
            instance.profile = uploaded.get("secure_url")

        # Handle social links
        social_fields = ['linkedin', 'github', 'twitter', 'website']
        social_data = {field: validated_data.pop(field, '') for field in social_fields}
        instance.social_links = {**(instance.social_links or {}), **social_data}

        # Update remaining fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the instance
        instance.save()

        # ✅ After successful save, delete the old image
        if uploaded and old_image_url:
            from urllib.parse import urlparse
            import os

            parsed = urlparse(old_image_url)
            public_id = os.path.splitext(parsed.path.split('/')[-1])[0]
            print(f"Deleting old image with public_id: {old_image_url}")
            print(f"Public ID: {uploaded.get('secure_url')}")
            cloudinary_destroy(public_id)

        return instance



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'name', 'username', 'email', 'role',
            'bio', 'profile', 'social_links', 'date_joined'
        ]
        read_only_fields = fields





from ..auth.otpsender import (LoginOtpSender
                              , forgetPasswordOtpSender,RegistrationOtpSender
                              ,UpdatePasswordOtpSender)

class RegistrationOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if  User.objects.filter(email=value).exists():
            print('user exist ')
            raise serializers.ValidationError("User with this email alredy exists.")
        return value

 
    
    def send_register_otp(self):
        email = self.validated_data['email']
        otp_sender = RegistrationOtpSender(email)
        otp = otp_sender.send()
        return otp




class Otpserializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            print('user not exist ')
            raise serializers.ValidationError("User with this email does not exist.")
        return value
   

    def send_forget_password_otp(self):
        email = self.validated_data['email']
        otp_sender = forgetPasswordOtpSender(email)
        otp = otp_sender.send()
        return otp
    def send_update_password_otp(self):
      
        email = self.validated_data['email']
        otp_sender = UpdatePasswordOtpSender(email)
        otp = otp_sender.send()
        return otp
    
    def send_login_otp(self):
        email = self.validated_data['email']
        otp_sender = LoginOtpSender(email)
        otp = otp_sender.send()
        return otp
    

    

# print('T'=="T")