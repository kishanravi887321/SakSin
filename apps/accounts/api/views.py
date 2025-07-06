from rest_framework.views import  APIView
from rest_framework.views  import  Response
from ..serializers import  UserRegistrationSerializer

class  RegisterView(APIView):
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return  Response({"msg":"creatd successfully"},status=201)
        return  Response(serializer.errors,status=400)
    