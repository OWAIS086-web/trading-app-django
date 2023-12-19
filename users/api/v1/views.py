from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser,MultiPartParser, FormParser

from users.models import *
from allauth.account.models import EmailAddress
from .auth_serializers import AccountAuthTokenSerializer
from .serializers import *
from users.models import *

from rest_framework import generics, status, response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


class MediaFilesUploadAPIView(generics.ListCreateAPIView):
    queryset = MediaFiles.objects.all()
    serializer_class = MediaFilesSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):    
        # Associate the uploaded file with the current user    
        try:
            # Find the Token object with the provided token value
            # token_obj = Token.objects.get(key=self.request.token)            
            # Access the user associated with the token
            # user = request.user
            # Create and save an UploadedFile object associated with the user
            serializer = MediaFilesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                file_type = request.data.get('file_type', None)
                if file_type =='Profile Pictures':
                    media_instance = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures').order_by('-updated_on').first()
                    profile_instance = UserProfile.objects.filter(user_id=request.user.id).first()
                    profile_instance.profile_pic = media_instance.media_file
                    profile_instance.updated_by = request.user
                    profile_instance.updated_on = timezone.now()
                    profile_instance.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Token.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # Token not found or invalid
            # return None
                

class CustomPasswordResetView(CreateAPIView):
    serializer_class = CustomPasswordResetSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)
       

class AccountTokenLoginAPIView(CreateAPIView):
    # serializer_class = AuthTokenSerializer
    serializer_class = AccountAuthTokenSerializer
    queryset = Token.objects.none()
    authentication_classes = []
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        fcm_device = serializer.validated_data.get('device', None)
        if fcm_device:
            from fcm_django.api.rest_framework import FCMDeviceSerializer
            from fcm_django.models import FCMDevice
            devices = FCMDevice.objects.filter(registration_id=fcm_device.get('registration_id'))
            if devices.exists():
                devices.update(user=user, active=True)
            else:
                try:
                    fcm_device_serializer = FCMDeviceSerializer(data=fcm_device, context={'request': request})
                    fcm_device_serializer.is_valid(raise_exception=True)
                    fcm_device_serializer.save(user=user)
                except Exception as err:
                    print('fcm error', err)
        user_serializer = AccountAuthUserSerializer(user)
        return Response({"token": token.key, "user": user_serializer.data})

class UserRegistrationAPIView(CreateAPIView):   
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = []       
        # email = request.data.get('email', None)
        # is_email = email_address_exists(email)
        # if is_email:
        #     return Response({
        #         'success': True,
        #         'message': f'Account created for {email}. Please check your email for OTP verification.'
        #     })
        # return Response({
        #     'success': False,
        #     'message': f'unexpected error while creating accounting for {email}.'
        # }, status=404)    

class VerifyEmailExistAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response({
                'success': False,
                'message': 'Email field required.'
            }, status=400)
        is_email = email_address_exists(email)
        if is_email:
            return Response({
                'success': True,
                'message': 'An account already exists with this email address.'
            })
        return Response({
            'success': False,
            'message': 'Email address not found.'
        }, status=404)
    
class VerifyOTPAPIView(APIView):
    # serializer_class = AccountAuthTokenSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        entered_otp = request.data.get('otp', None)
        if not email:
            return Response({
                'success': False,
                'message': 'email field required.'
            }, status=400)
        
        if not entered_otp:
            return Response({
                'success': False,
                'message': 'otp field required.'
            }, status=400)
                
        user = User.objects.filter(email=email).first()
        if user is not None:
            Profile = UserProfile.objects.filter(user_id=user.id).first()
            email_address = EmailAddress.objects.get(user=user, primary=True)
            # Check if OTP is valid and not expired
            if Profile.otp == entered_otp and Profile.otp_expiry_time > timezone.now():
                # OTP verification successful
                user.is_active = True
                user.save()        

                email_address.verified  = True
                email_address.save()

                return Response({
                    'success': True,
                    'message': 'OTP verified successfully.'
                })            
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid OTP or OTP has expired. Please try again.'
                }, status=404)            
        else:
            return Response({
                'success': False,
                'message': 'Invalid Email address. Please try again.'
            }, status=404)
        
class UpdateUserProfileAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        user = User.objects.filter(email=email).first()
        if user is not None:
            # Get the associated Email Address
            # Profile = EmailAddress()
            try:
                email_address = EmailAddress.objects.get(user=user, primary=True)
                email_address.verified  = True
                email_address.save()
            except EmailAddress.DoesNotExist:
                # Handle the case where the EmailAddress object doesn't exist or has been deleted
                try:
                    setup_user_email(request, user, [])
                    email_address = EmailAddress.objects.get(user=user, primary=True)
                    email_address.verified  = True
                    email_address.save()                        
                except Exception as err:
                    print(err)
                    print('setup user email error')            
            
            # Profile = UserProfile.objects.filter(user_id=user.id).first()
            Profile = UserProfile.objects.filter(user=user).first()
            Profile.display_name = request.data.get('display_name', '-') 
            Profile.prefix = request.data.get('prefix', '-')
            Profile.first_name = request.data.get('first_name', '-')
            Profile.middle_name = request.data.get('middle_name', '-')
            Profile.last_name = request.data.get('last_name', '-')
            Profile.biography = request.data.get('biography', '-')
            Profile.telephone = request.data.get('telephone', '-')
            Profile.cell = request.data.get('cell', '-')
            Profile.fax = request.data.get('fax', '-')
            Profile.website = request.data.get('website', '-')
            Profile.twitter = request.data.get('twitter', '-')
            Profile.skype = request.data.get('skype', '-')
            Profile.linkedin = request.data.get('linkedin', '-')
            Profile.facebook = request.data.get('facebook', '-')
            Profile.instagram = request.data.get('instagram', '-')
            Profile.unit = request.data.get('unit', '-')
            Profile.street = request.data.get('street', '-')
            Profile.postal_code = request.data.get('postal_code', '-')
            Profile.updated_by = user
            Profile.updated_on = timezone.now()
            Profile.save()
            return Response({
                'success': True,
                'message': 'user profile updated successfully.'
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid Email address. Please try again.'
            }, status=404)
                
class ResendOTPVerificationAPIView(APIView):
    # serializer_class = AccountAuthTokenSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        if not email:
            return Response({
                'success': False,
                'message': 'email field required.'
            }, status=400)
                        
        user = User.objects.filter(email=email).first()
        if user is not None:
            Profile = UserProfile.objects.filter(user_id=user.id).first()
            # Generate a new OTP
            otp = random.randint(100000, 999999)
            # Update the OTP and expiry time in the profile
            Profile.otp = otp
            Profile.otp_expiry_time = timezone.now() + timedelta(minutes=5)
            # Profile.updated_by = uid
            Profile.updated_on = timezone.now()
            Profile.save()
            # Resend the OTP via email
            send_otp_email(user=user, otp=otp,generated=timezone.now(),validtill=(timezone.now()+ timedelta(minutes=5)))
            return Response({
                'success': True,
                'message': 'OTP has been resent successfully.'
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid Email address. Please try again.'
            }, status=404)
        
class AccountAuthProfileDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = AccountAuthUserSerializer
    queryset = User.objects.none()

    def get_serializer_class(self):
        # if self.request.user.user_type == User.USER_TYPE_DOCTOR:
        #     return AccountAuthUserDoctorSerializer
        # elif self.request.user.user_type == User.USER_TYPE_PATIENT:
        #     return AccountAuthUserPatientSerializer
        # else:
        #     return AccountAuthUserSerializer
        return AccountAuthUserSerializer
    
    def get_object(self):
        return self.request.user
            
class AccountDeleteAPIView(DestroyAPIView):
    serializer_class = AccountAuthUserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.none()

    def get_object(self):
        return self.request.user