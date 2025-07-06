from django.urls import path
from  .views  import  RegisterView,CustomTokenObtainPairView

urlpatterns=[
    path('register/',RegisterView.as_view(),name='reg-view'),
    path('login/',CustomTokenObtainPairView.as_view(),name='login-view'),

]