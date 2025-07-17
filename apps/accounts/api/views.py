from rest_framework import generics, status
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..serializers import(
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UpdatePasswordSerializer,
    Otpserializer,RegistrationOtpSerializer,
    LoginGoogleAuthSerializer,
    ForgetPasswordSerializer,
    UsernameCheckSerializer,UserProfileSerializer,ProfileSerializer
    

    
    
    
    
    
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
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileview(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user profile",
        responses={200: UserProfileSerializer}
    )
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Profile updated successfully"}, status=status.HTTP_200_OK)

# 3. Update Password View: Using UpdateAPIView with the current user as the object
class UpdatePasswordView(generics.UpdateAPIView):
    serializer_class = UpdatePasswordSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Allow file uploads if needed
    queryset = User.objects.all()  # Required for UpdateAPIView

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user
   
    def update(self, request, *args, **kwargs):
        # Use partial update if necessary
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "Password updated successfully"}, status=status.HTTP_200_OK)

# 4. Profile Image Upload View: Using UpdateAPIView to update the current user's profile image


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
    

