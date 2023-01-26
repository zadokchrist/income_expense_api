from django.shortcuts import render
from rest_framework import generics,views
from .serializers import RegisterSerializer,EmailVerificationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class RegisterViews(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        currentsites = get_current_site(request).domain
        relativeurl = reverse('verify-email')
        absurl = 'http://'+currentsites+relativeurl+'?token='+str(token)
        email_body ='Hi '+user.username+',\n Use the link below to verify your email.\n'+absurl
        data ={
            'body' : email_body,
            'domain' :absurl,
            'email' : user.email,
            'email_subject' : 'VERIFY EMAIL'
        }
        Util.sendemail(data)
        return Response(user_data,status=status.HTTP_201_CREATED)
    
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',
                                           type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            print('***********************************')
            print(payload['user_id'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_varified:
                user.is_varified=True
                user.save()
            return Response({'email': 'successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as expired:
            return Response({'error' : 'activation link has expired'},status=status.HTTP_200_OK)
        except jwt.DecodeError as e:
            print('**********************************************')
            print(e)
            return Response({'error' : 'invalid token request new one '+str(e)},status=status.HTTP_400_BAD_REQUEST)
        