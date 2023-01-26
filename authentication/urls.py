from django.urls import path
from .views import RegisterViews,VerifyEmail

urlpatterns = [
    path('register/',RegisterViews.as_view(),name='register'),
    path('verify-email/',VerifyEmail.as_view(),name='verify-email')
]