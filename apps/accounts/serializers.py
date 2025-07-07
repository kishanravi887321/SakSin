
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


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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

        try:
            # Check if it's an email or username
            if '@' in login_value:
                user = User.objects.get(email=login_value)
            else:
                print("username",login_value)
                user = User.objects.get(username=login_value)
        except User.DoesNotExist:
            raise serializers.ValidationError("user doesnt exist")

        if not user.check_password(password):
            raise serializers.ValidationError("password is incorrect")

        # Inject the actual username into attrs for token creation
        attrs['username'] = user.username
        self.user = user

        # Let super() generate the token using username
        data = super().validate(attrs)

        # Add custom claims
        data['username'] = user.username
        data['email'] = user.email

        return data


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