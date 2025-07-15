from django.urls import path
from  .views  import  (RegisterView,CustomTokenObtainPairView,UpdatePasswordView,ProfileImageUploadView
                       ,AuthForRegistration
                          ,AuthforUpdatePassword
                          ,AuthforForgetPassword
                       
                       )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='reg-view'),
    path('login/',CustomTokenObtainPairView.as_view(),name='login-view'),
    path('auth/update-password/', AuthforUpdatePassword.as_view(), name='auth-update-password-view'),
    path('auth/register/', AuthForRegistration.as_view(), name='auth-register-view'),
    path('auth/forget-password/', AuthforForgetPassword.as_view(), name='auth-forget-password-view'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),
    path('update-profile/', ProfileImageUploadView.as_view(), name='profile-image-upload-view')
    ]