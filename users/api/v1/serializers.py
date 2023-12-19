from rest_framework import serializers
from users.models import *
from django.utils import timezone
import random
from datetime import timedelta
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

User = get_user_model()

def send_otp_email(user, otp,generated,validtill):
    subject = 'Priority Gold Plus - OTP Verification'
    context = {'otp': otp,'generated': generated, 'valid': validtill}
    html_content = render_to_string('account/email/otp_verify_message.html',context)
    message = strip_tags(html_content)    
    # message = f'Hello, For verification of your account, use this OTP: {otp}'
    email = EmailMultiAlternatives(subject,message,settings.EMAIL_HOST_USER,to=[user.email])
    email.attach_alternative(html_content,"text/html")    
    # email = EmailMessage(subject, message, to=[user.email])
    email.send()


class MediaFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaFiles
        fields = '__all__'


class CustomPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        reset_form = ResetPasswordForm(data={'email': value})
        if not reset_form.is_valid():
            raise serializers.ValidationError(reset_form.errors)
        return value

    def save(self, **kwargs):
        reset_form = ResetPasswordForm(data=self.validated_data)
        if reset_form.is_valid():
            reset_form.save(request=self.context.get('request'))


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            }
        }

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        uid = User.objects.get(pk=1)
        user = User(
            email=validated_data.get('email'),
            username=generate_unique_username([
                validated_data.get('email'),
                'user'
            ])
        )
        user.created_by = uid
        user.created_on = timezone.now()
        user.updated_by = uid
        user.updated_on = timezone.now()
        user.set_password(validated_data.get('password'))
        user.save()

        otp = random.randint(100000, 999999)
        Profile = UserProfile()
        Profile.user = user            
        Profile.display_name="-" 
        Profile.prefix="-"
        Profile.first_name="-"
        Profile.middle_name="-"
        Profile.last_name="-"
        Profile.biography="-"
        Profile.telephone="+1" 
        Profile.cell="+1"
        Profile.fax="+1"
        Profile.website="-"
        Profile.twitter="-"
        Profile.skype="-"
        Profile.linkedin="-"
        Profile.facebook="-"
        Profile.instagram="-" 
        Profile.unit="-"
        Profile.street="-"
        Profile.postal_code="-" 
        Profile.otp = otp
        Profile.otp_expiry_time = timezone.now() + timedelta(minutes=5)  # Set OTP expiration time            
        Profile.created_by = uid
        Profile.created_on = timezone.now()
        Profile.updated_by = uid
        Profile.updated_on = timezone.now()
        Profile.save()

        send_otp_email(user=user, otp=otp,generated=timezone.now(),validtill=(timezone.now()+ timedelta(minutes=5)))

        request = self._get_request()
        setup_user_email(request, user, [])
        return user

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()
    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ['id', 'email', 'name']


class UserProfileRegistrationSerializer(serializers.ModelSerializer):
    # date_of_birth = serializers.DateField(required=True, format='%m-%d-%Y', input_formats=['%m-%d-%Y', 'iso-8601'])
    # phone_number = serializers.CharField(required=True)
    # primary_practice_address = serializers.CharField(required=True)
    # state = serializers.CharField(required=True)
    # city = serializers.CharField(required=True)
    # zip_code = serializers.CharField(required=True)
    # dental_license_number = serializers.CharField(required=True)
    # license_state = serializers.CharField(required=True)
    # degree = serializers.CharField(required=True)
    # npi_number = serializers.CharField(required=True)
    # graduation_year = serializers.IntegerField(required=True)
    # country = CountryField(country_dict=True, required=True)
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'user': {
                'read_only': True
            },
            # 'approval_status': {
            #     'read_only': True
            # }
        }

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserProfileRegistrationSerializer(source='user_profile')
    # password = serializers.CharField(max_length=32, required=True, write_only=True)
    class Meta:
        model = User
        fields = ('id','username','email', 'password', 'profile')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'email': {
                'required': True,
                'allow_blank': False,
            },
            'user': {
                'read_only': True,
            }
        }

    def validate_password(self, password):
        if len(password) < 6:
            raise serializers.ValidationError(
                _("Password too short. It must contain at least 6 alpha-numeric characters."),
                code='password_too_short',
            )
        if password.isdigit():
            raise serializers.ValidationError(
                _("Password must contain at least 1 character."),
                code='password_entirely_numeric',
            )
        if password.isalpha():
            raise serializers.ValidationError(
                _("Password must contain at least 1 digit."),
                code='password_entirely_characters',
            )

        return password

    def _get_request(self):
        request = self.context.get('request')
        if request and not isinstance(request, HttpRequest) and hasattr(request, '_request'):
            request = request._request
        return request

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def create(self, validated_data):
        uid = User.objects.get(pk=1)
        email = validated_data.get('email')
        # name = f'{first_name} {last_name}'.strip()
        profile = validated_data.pop('user_profile')
        # username =  validated_data.get('email') #generate_unique_username([email, 'user'])
        user = User(
            email=email #            username=username,
        )
        user.username = validated_data.get('email')
        user.created_by = uid
        user.created_on = timezone.now()
        user.updated_by = uid
        user.updated_on = timezone.now() 
        user.set_password(validated_data.get('password'))
        user.save()

        if user:
            try:
                UserProfile.objects.create(user=user, **profile)
                # Profile = UserProfile.objects.filter(user_id=request.user).first()
                Profile = UserProfile.objects.filter(user=user).first()
                otp = random.randint(100000, 999999)
                # Profile.user = user            
                Profile.display_name="-" 
                Profile.prefix="-"
                Profile.first_name="-"
                Profile.middle_name="-"
                Profile.last_name="-"
                Profile.biography="-"
                Profile.telephone="+1" 
                Profile.cell="+1"
                Profile.fax="+1"
                Profile.website="-"
                Profile.twitter="-"
                Profile.skype="-"
                Profile.linkedin="-"
                Profile.facebook="-"
                Profile.instagram="-" 
                Profile.unit="-"
                Profile.street="-"
                Profile.postal_code="-" 
                Profile.otp = otp
                Profile.otp_expiry_time = timezone.now() + timedelta(minutes=5)  # Set OTP expiration time            
                Profile.created_by = uid
                Profile.created_on = timezone.now()
                Profile.updated_by = uid
                Profile.updated_on = timezone.now()
                Profile.save()

                send_otp_email(user=user, otp=otp,generated=timezone.now(),validtill=(timezone.now()+ timedelta(minutes=5)))

            except Exception as err:
                print(err)
        request = self._get_request()
        try:
            setup_user_email(request, user, [])
        except Exception as err:
            print(err)
            print('setup user email error')
        return user
        

    def save(self, request=None):
        """rest_auth passes request so we must override to accept it"""
        return super().save()


class AccountAuthUserSerializer(serializers.ModelSerializer):
    # subscription = SubscriptionDetailSerializer(source='get_subscription', read_only=True, default=None)

    class Meta:
        model = User
        fields = ('id', 'email', 'is_active')
        extra_kwargs = {
            'email': {
                'read_only': True
            },
            'is_active': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        res = super(self.__class__, self).to_representation(instance)
        try:
            res['profile'] = UserProfileSerializer(instance.user_profile).data
        except UserProfile.DoesNotExist:
            res['profile'] = None

        return res

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        # fields = ('id','display_name','first_name', 'biography', 'profile_pic','telephone','street')
        fields = '__all__'

    def update(self, validated_data):
        uid = User.objects.get(pk=1)
        email = validated_data.get('email')
        # name = f'{first_name} {last_name}'.strip()
        profile = validated_data.pop('user_profile')
        user = User(email=email)
        if user:
            try:
                # UserProfile.objects.create(user=user, **profile)
                # Profile = UserProfile.objects.filter(user_id=request.user).first()
                Profile = UserProfile.objects.filter(user=user).first()
                Profile.display_name = validated_data.get('display_name') 
                Profile.prefix = validated_data.get('prefix')
                Profile.first_name = validated_data.get('first_name')
                Profile.middle_name = validated_data.get('middle_name')
                Profile.last_name = validated_data.get('last_name')
                Profile.biography = validated_data.get('biography')
                Profile.telephone = validated_data.get('telephone')
                Profile.cell = validated_data.get('cell')
                Profile.fax = validated_data.get('fax')
                Profile.website = validated_data.get('website')
                Profile.twitter = validated_data.get('twitter')
                Profile.skype = validated_data.get('skype')
                Profile.linkedin = validated_data.get('linkedin')
                Profile.facebook = validated_data.get('facebook')
                Profile.instagram = validated_data.get('instagram')
                Profile.unit = validated_data.get('unit')
                Profile.street = validated_data.get('street')
                Profile.postal_code = validated_data.get('postal_code')
                Profile.updated_by = user.id
                Profile.updated_on = timezone.now()
                Profile.save()

            except Exception as err:
                print(err)

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'

#     def validate(self, data):
#         if data["email"] == "":
#             raise serializers.ValidationError('Our system requires the "Email Address" However, it seems that the email you entered is not valid.')
#         if data["password1"] != data["password2"]:
#             raise serializers.ValidationError('Our system requires that the "Password" and "Confirm Password" fields must match exactly to ensure the security and integrity of your account. However, it seems that the passwords you entered do not match.')
#         return data

#     def create(self, validated_data):
#         uid = User.objects.get(pk=1)
#         user_instance = User.objects.create(            
#             username = validated_data['email'],
#             email = validated_data['email'],
#             created_by = uid,
#             created_on = timezone.now(),
#             updated_by = uid,
#             updated_on = timezone.now(),
#         )
#         user_instance.set_password(validated_data['password1'])
#         user_instance.save()

#         otp = random.randint(100000, 999999)
#         Profile = UserProfile()
#         Profile.user = user_instance            
#         Profile.display_name="-" 
#         Profile.prefix="-"
#         Profile.first_name="-"
#         Profile.middle_name="-"
#         Profile.last_name="-"
#         Profile.biography="-"
#         Profile.telephone="+1" 
#         Profile.cell="+1"
#         Profile.fax="+1"
#         Profile.website="-"
#         Profile.twitter="-"
#         Profile.skype="-"
#         Profile.linkedin="-"
#         Profile.facebook="-"
#         Profile.instagram="-" 
#         Profile.unit="-"
#         Profile.street="-"
#         Profile.postal_code="-" 
#         Profile.otp = otp
#         Profile.otp_expiry_time = timezone.now() + timedelta(minutes=5)  # Set OTP expiration time            
#         Profile.created_by = uid
#         Profile.created_on = timezone.now()
#         Profile.updated_by = uid
#         Profile.updated_on = timezone.now()
#         Profile.save()

#         send_otp_email(user=user_instance, otp=otp,generated=timezone.now(),validtill=(timezone.now()+ timedelta(minutes=5)))

#         return user_instance    


# class EmailInvitationSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)

# class AppStoreLinkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AppStoreLink
#         fields = '__all__'