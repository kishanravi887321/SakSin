from django.contrib.auth import  get_user_model
from rest_framework import  serializers

User=get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    role=serializers.CharField(required=False)

    class Meta:
        model=User
        fields=['username','password','email','role','bio']

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    