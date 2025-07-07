from rest_framework.views import  APIView
from rest_framework.generics import GenericAPIView
from rest_framework.views  import  Response
from rest_framework.permissions import IsAuthenticated
from ..serializers import  UserRegistrationSerializer,CustomTokenObtainPairSerializer,UpdatePasswordSerializer


class  RegisterView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response({"msg":"creatd successfully"},status=201)
        return  Response(serializer.errors,status=400)
    
class CustomTokenObtainPairView(APIView):
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid():
          
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)
    
class UpdatePasswordView(GenericAPIView):
   permission_classes = [IsAuthenticated]
   serializer_class = UpdatePasswordSerializer

   def put(self,request):
       serializer = self.get_serializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           return Response({"msg": "Password updated successfully"}, status=200)    
       return Response(serializer.errors, status=400)
    