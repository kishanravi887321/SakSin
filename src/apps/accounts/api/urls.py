from django.urls import path
from  .views  import  (RegisterView,CustomTokenObtainPairView,UpdatePasswordView,ProfileImageUploadView
                       ,AuthForRegistration
                          ,AuthforUpdatePassword
                          ,AuthforForgetPassword
                           ,GoogleLoginView,
                            AuthforLogin,
                            ForgetPasswordView,
                            UsernameCheckView,ViewUser,
                            UpdateProfileView,
                            FeedChatifyView,Doctor
                       )
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='reg-view'),
    path('doctor/', Doctor.as_view(), name='doctor-view'),
    path('login/',CustomTokenObtainPairView.as_view(),name='login-view'),
    path('check-username/', UsernameCheckView.as_view(), name='username-check-view'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login-view'),
    path('auth/login/', AuthforLogin.as_view(), name='auth-login-view'),
    path('auth/update-password/', AuthforUpdatePassword.as_view(), name='auth-update-password-view'),
    path('auth/register/', AuthForRegistration.as_view(), name='auth-register-view'),
    path('auth/forget-password/', AuthforForgetPassword.as_view(), name='auth-forget-password-view'),
    path('update-password/', UpdatePasswordView.as_view(), name='update-password-view'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password-view'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh-view'),
    path('update-profile/', ProfileImageUploadView.as_view(), name='profile-image-upload-view'),
    path('profile/', ViewUser.as_view(), name='view-user'),
    path('profile/update/', UpdateProfileView.as_view(), name='update-profile-view'),
    path('chat/feed/', FeedChatifyView.as_view(), name='feed-chatify-view'),


    ]