from rest_framework import generics, status
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers import(
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UpdatePasswordSerializer,
    ProfileImageUploadSerializer,Otpserializer,RegistrationOtpSerializer,

    
    
    
    
    
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
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

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

class AuthForRegistration(APIView):
 
    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=RegistrationOtpSerializer)
    def post(self, request):
        serializer = RegistrationOtpSerializer(data=request.data)
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
    

