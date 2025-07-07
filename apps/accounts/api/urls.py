from django.urls import path
from  .views  import  RegisterView,CustomTokenObtainPairView,UpdatePasswordView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='reg-view'),
    path('login/',CustomTokenObtainPairView.as_view(),name='login-view'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),


]