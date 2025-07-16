from django.db import models
from django.contrib.auth.models import  AbstractBaseUser ,BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self,username,email,password=None,role='user',bio=None):
        if not email:
            raise ValueError('email field must have to provide')
        if '@' in username:
            raise ValueError('username should not contain @')   
        user=self.model(
            username=username,
            email=self.normalize_email(email),
            role=role,
            bio=bio
        )

        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,username,email,password):
        user=self.create_user(
            username=username,
            email=email,
            password=password,
            role='admin'
                              
                              )
        user.is_admin=True
        user.save(using=self._db)

        return user 

# Create your models here.
class User(AbstractBaseUser):
    username=models.CharField(unique=True,max_length=20,blank=True,null=True)
    email=models.EmailField(unique=True)
    role=models.CharField(max_length=20,null=True,blank=True,default='student')
    bio=models.TextField(max_length=200,null=True,blank=True)

    profile=models.URLField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()
    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin
