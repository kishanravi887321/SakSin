from rest_framework import generics, status
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers import(
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UpdatePasswordSerializer,
    ProfileImageUploadSerializer,Otpserializer,RegistrationOtpSerializer,
    LoginGoogleAuthSerializer,
    ForgetPasswordSerializer,
    UsernameCheckSerializer
    ,ViewUserSerializer
    ,ProfileUpdateSerializer
    ,FeedChatifySerializer

    
    
    
    
    
    )
from ..profile_doc import profile_image_upload_doc
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from ..models import User  # Adjust this import to match your project structure

# 1. Registration View: CreateAPIView auto-documents the request body
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

# 2. Custom Token Obtain Pair View: Using GenericAPIView with a serializer
class CustomTokenObtainPairView(generics.GenericAPIView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Will automatically raise a 400 error if not valid
        x=serializer.is_valid()
        if not x:
            return Response({"msg":"password incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ForgetPasswordView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=ForgetPasswordSerializer,
        operation_description="Reset password using OTP"
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"msg": "Password reset successfully"}, status=status.HTTP_200_OK)      
class UsernameCheckView(generics.GenericAPIView):
    serializer_class = UsernameCheckSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Check if username is available",
        responses={200: "Username is available", 400: "Username already exists"}
    )
    def post(self, request, *args, **kwargs):
     serializer = self.get_serializer(data=request.data)
    
     if serializer.is_valid():
        # Username is available (passed validation)
        return Response({"available": True, "msg": "Username is available"}, status=status.HTTP_200_OK)
     else:
        # Username already exists (failed validation)
        return Response({"available": False, "msg": "Username already exists"}, status=status.HTTP_200_OK)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=LoginGoogleAuthSerializer,
        operation_description="Login using Google ID Token"
    )
    def post(self, request):
        serializer = LoginGoogleAuthSerializer(data=request.data)
        print("Request data: during google login", request.data,"request",request)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# 3. Update Password View: Using UpdateAPIView with the current user as the object
class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads if needed
    queryset = User.objects.all()  # Required for UpdateAPIView

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user
    @swagger_auto_schema(
        operation_description="Upload profile image",
        request_body=ProfileImageUploadSerializer  # ✅ important!
    )
    def update(self, request, *args, **kwargs):
        # Use partial update if necessary
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Password updated successfully"}, status=status.HTTP_200_OK)

# 4. Profile Image Upload View: Using UpdateAPIView to update the current user's profile image
class ProfileImageUploadView(generics.UpdateAPIView):
    serializer_class = ProfileImageUploadSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()  # Required for UpdateAPIView

    def get_object(self):
        # Return the currently authenticated user   
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Pass instance and request data to the serializer; using partial update in case not all fields are provided
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Assuming the user model's "profile" attribute gets updated in the serializer's update() method
        return Response(
            {"msg": "Profile image updated successfully", "url": instance.profile},
            status=status.HTTP_200_OK
        )
class Doctor(APIView):
    permission_classes = [AllowAny]
    def get(self,req):
        print("checked successfully")
        return Response({"msg": "Doctor cool"}, status=status.HTTP_200_OK)

class AuthForRegistration(APIView):
 
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegistrationOtpSerializer)
    def post(self, request):
        serializer = RegistrationOtpSerializer(data=request.data)
        print("Request data: during registration", request.data,"request",request)
        if serializer.is_valid():
            serializer.send_register_otp()
            return Response({"msg": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AuthforUpdatePassword(APIView):
    permission_classes=[IsAuthenticated]
    
    @swagger_auto_schema(request_body=Otpserializer)
    def post(self,request):
        serializer= Otpserializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.send_update_password_otp()
            return Response({"msg": "OTP sent successfully"}, status=status.HTTP_200_OK)   
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthforForgetPassword(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=Otpserializer)
    def post(self, request):
        serializer = Otpserializer(data=request.data)
        if serializer.is_valid():
            serializer.send_forget_password_otp()
            return Response({"msg": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
class AuthforLogin(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=Otpserializer)
    def post(self, request):
        serializer = Otpserializer(data=request.data)
        if serializer.is_valid():
            serializer.send_login_otp()
            return Response({"msg": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ViewUser(generics.RetrieveAPIView):
    serializer_class = ViewUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()  # Required for RetrieveAPIView

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

    @swagger_auto_schema(
        operation_description="Retrieve user profile",
        responses={200: ProfileImageUploadSerializer}
    )
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        operation_description="Update user profile",
        request_body=ProfileUpdateSerializer
    )
    def update(self, request, *args, **kwargs):
        print(request.data, "the data is ")

        data = request.data.copy()
        # Make sure to get raw values, not lists (if coming from form-data)
        social_links = {
            "linkedin": data.pop("linkedin", None),
            "github": data.pop("github", None),
            "twitter": data.pop("twitter", None),
            "website": data.pop("website", None),
        }

        # Remove None values
        social_links = {k: v for k, v in social_links.items() if v is not None}
        data["social_links"] = social_links

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"msg": "Profile updated successfully"}, status=status.HTTP_200_OK)


import requests

class FeedChatifyView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Feed Chatify",
        request_body=FeedChatifySerializer
    )
    def post(self, request):
        serializer = FeedChatifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "Chatify feed update failed"}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        email = user.email
        raw_text = serializer.validated_data.get("content")
        print(raw_text, "the raw text is ")
        if len(raw_text) > 10000:
            print('exceed')
            return Response({"msg": "Content exceeds maximum length of 6000 characters"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.post(
                "http://localhost:8005/chat/feed/",
                json={"email": email, "raw_text": raw_text},timeout=30
            )
            if response.status_code == 200:
                print(response.json(), "the response is ")
                return Response({"msg": "Chatify feed updated successfully","data":
                                 response.json()}, status=status.HTTP_200_OK)
            else:
                return Response({"msg": "Failed to update Chatify feed"}, status=status.HTTP_400_BAD_REQUEST)


        except requests.exceptions.RequestException as e:
            return Response({"msg": "internal server error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)