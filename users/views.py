from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.views.generic import DetailView, RedirectView, UpdateView, CreateView, FormView
from django.utils import timezone

from .forms import UserRegisterForm,StaffRegisterForm,AdminRegisterForm, UserProfileForm,UserCreationForm,UserChangeForm,UpdateUserForm, UpdateProfileForm,UpdateMediaForm

from django.contrib import messages
import random
from datetime import timedelta
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from users.models import User, UserProfile,MediaFiles
from allauth.account.models import EmailAddress

from django.utils.html import strip_tags
from django.conf import settings 

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.urls import reverse, reverse_lazy

from allauth.account import app_settings as allauth_settings
from allauth.account.forms import ResetPasswordForm
from allauth.utils import email_address_exists, generate_unique_username
# from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


User = get_user_model()

def send_otp_email(user, otp, generated, validtill):
    subject = 'Priority Gold Plus - OTP Verification'
    context = {'otp': otp, 'generated': generated, 'valid': validtill}
    html_content = render_to_string('account/email/otp_verify_message.html', context)
    message = strip_tags(html_content)
    email = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, to=[user.email])
    email.attach_alternative(html_content, "text/html")
    email.send()

def sign_up(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form': form, "head_title": "User Registration | Priority Gold Plus"}
        return render(request, 'account/signup.html', context)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if allauth_settings.UNIQUE_EMAIL and email_address_exists(email):
                messages.error(request, 'A user is already registered with this e-mail address.')
                context = {'form': form, "head_title": "User Registration | Priority Gold Plus"}
                print(context)
                return render(request, 'account/signup.html', context)

            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                context = {'form': form, "head_title": "User Registration | Priority Gold Plus"}
                return render(request, 'account/signup.html', context)

            uid = User.objects.get(pk=1)
            user_instance = form.save(commit=False)
            user_instance.username = email  # Use email as username
            user_instance.created_by = uid
            user_instance.created_on = timezone.now()
            user_instance.updated_by = uid
            user_instance.updated_on = timezone.now()
            user_instance.save()

            otp = random.randint(100000, 999999)
            Profile = UserProfile()
            Profile.user = user_instance
            Profile.display_name = "-"
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
            Profile.otp = otp
            Profile.otp_expiry_time = timezone.now() + timedelta(minutes=5)
            Profile.created_by = uid
            Profile.created_on = timezone.now()
            Profile.updated_by = uid
            Profile.updated_on = timezone.now()
            Profile.save()

            send_otp_email(user=user_instance, otp=otp, generated=timezone.now(), validtill=(timezone.now() + timedelta(minutes=5)))
            user_email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {user_email}. Please check your email for OTP verification.')

            try:
                setup_user_email(request, user_instance, [])
            except Exception as err:
                print(err)
                print('setup user email error')

            uidb64 = urlsafe_base64_encode(force_bytes(user_instance.pk))
            token = default_token_generator.make_token(user_instance)
            return redirect('users:user_otp_verification', uidb64=uidb64, token=token)

        else:
            messages.error(request, 'check again information form is not')
            context = {'form': form, "head_title": "User Registration | Priority Gold Plus"}
            return render(request, 'account/signup.html', context)

    return render(request, 'account/signup.html', {"head_title": "User Registration | Priority Gold Plus"})

class opt_verification_view(View):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            context = {'uidb64': uidb64, 'token': token}
            return render(request, 'account/otp_verification.html', context)

        messages.error(request, 'Invalid OTP verification link or token.')
        return redirect('register')

    def post(self, request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if request.method == 'POST':
                digit1 = request.POST.get('digit1')
                digit2 = request.POST.get('digit2')
                digit3 = request.POST.get('digit3')
                digit4 = request.POST.get('digit4')
                digit5 = request.POST.get('digit5')
                digit6 = request.POST.get('digit6')
                entered_otp = digit1 + digit2 + digit3 + digit4 + digit5 + digit6

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

                # Get the associated profile
                # Profile = UserProfile()
                try:
                    Profile = UserProfile.objects.filter(user_id=user.id).first()
                    if Profile.otp == entered_otp and Profile.otp_expiry_time > timezone.now():
                        # OTP verification successful
                        user.is_active = True
                        user.save()
                        # Log in the user
                        user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend attribute
                        login(request, user)

                        messages.success(request, 'OTP verified successfully. You have been logged in.')
                        return redirect('users:edit_profile')
                    else:
                        messages.error(request, 'Invalid OTP or OTP has expired. Please try again.')
                        return redirect('users:user_otp_verification', uidb64=uidb64, token=token)
                except UserProfile.DoesNotExist:
                    # Handle the case where the UserProfile object doesn't exist or has been deleted                 
                    context = {'uidb64': uidb64, 'token': token}
                    return render(request, 'account/otp_verification.html', context)
            else:
                context = {'uidb64': uidb64, 'token': token}
                return render(request, 'account/otp_verification.html', context)

        # Return an HTTP response in case of invalid OTP verification link or token
        messages.error(request, 'Invalid OTP verification link or token.')
        return redirect('register')

# class settings_view(SuccessMessageMixin, PasswordChangeView):
#     context = {"head_title": "User Registration | Priority Gold Plus"}
#     # data = {'form': form,"head_title": "Registration | Priority Gold"}
#     return render(request, 'account/settings.html', context)
#     # template_name = 'account/settings.html'
#     # success_message = "Successfully changed your password"
#     # success_url = reverse_lazy('password_change')

def settings_view(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Account Settings | Priority Gold Plus"}
    return render(request, "account/accountsettings.html", context)


def resend_otp(request, uidb64=None, token=None):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.filter(email=email).first()
            if user is not None:
                Profile = UserProfile.objects.filter(user_id=user.id).first()
                # profile = user.UserProfile
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

                messages.success(request, 'OTP has been resent successfully.')
                # context = {'uidb64': uidb64, 'token': token}
                # return redirect('users:user_otp_verification', context)
                return redirect('users:user_otp_verification', uidb64=uidb64, token=token)
        except User.DoesNotExist:
            pass

    return render(request, 'account/resend_otp.html', {'uidb64': uidb64, 'token': token})


def user_registration_view(request):
    if request.method == 'GET':
        form  = UserRegisterForm()
        context = {'form': form,"head_title": "User Registration | Priority Gold Plus"}
        # data = {'form': form,"head_title": "Registration | Priority Gold"}
        return render(request, 'account/signup.html', context)
    
    if request.method == 'POST':
        form  = UserRegisterForm(request.POST)
        if form.is_valid():
            uid = User.objects.get(pk=1)
            model_instance = form.save(commit=False)
            model_instance.created_by = uid
            model_instance.created_on = timezone.now()
            model_instance.updated_by = uid
            model_instance.updated_on = timezone.now()
            # Generate plain text output using the as_table() method
            # form_output = model_instance.as_table()
            # Print the form output
            # print(form_output)            
            model_instance.save()
            # form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('edit_profile')
        else:
            print('User Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form,"head_title": "User Registration | Priority Gold Plus"}
            # data = {'form': form,"head_title": "Registration | Priority Gold"}
            return render(request, 'account/signup.html', context)
    return render(request, 'account/signup.html', {"head_title": "Registration | Priority Gold Plus"})

# Registration view for staff
def staff_registration_view(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_by = request.user
            model_instance.created_on = timezone.now()
            model_instance.updated_by = request.user
            model_instance.updated_on = timezone.now()
            # Generate plain text output using the as_table() method
            # form_output = model_instance.as_table()
            # Print the form output
            # print(form_output)            
            model_instance.save()
            # form.save()            
            # Additional logic or redirect here
            user = form.cleaned_data.get('username')
            messages.success(request, 'Staff Account was created for ' + user)
            return redirect('home')  # Redirect to a success page
        else:
            print('Staff Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form,"head_title": "Staff Registration | Priority Gold Plus"}
            return render(request, 'account/signup.html', context)
    else:
        form = StaffRegisterForm()
        context = {'form': form,"head_title": "Staff Registration | Priority Gold Plus"}
        # data = {'form': form,"head_title": "Registration | Priority Gold"}
        return render(request, 'account/signup.html', context)

# Registration view for admin
def admin_registration_view(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_by = request.user.id
            model_instance.created_on = timezone.now()
            model_instance.updated_by = request.user.id
            model_instance.updated_on = timezone.now()
            # Generate plain text output using the as_table() method
            # form_output = model_instance.as_table()
            # Print the form output
            # print(form_output)
            model_instance.save()
            # form.save()            
            # Additional logic or redirect here
            user = form.cleaned_data.get('username')
            messages.success(request, 'Staff Account was created for ' + user)
            return redirect('home')  # Redirect to a success page
        else:
            print('Admin Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form,"head_title": "Admin Registration | Priority Gold Plus"}
            return render(request, 'account/signup.html', context)
    else:
        form = AdminRegisterForm()
        context = {'form': form,"head_title": "Admin Registration | Priority Gold Plus"}
        # data = {'form': form,"head_title": "Registration | Priority Gold"}
        return render(request, 'account/signup.html', context)

@login_required    
# Registration view for staff
def profile_view(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        Profile = UserProfile.objects.filter(user_id=request.user).first()
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=Profile)
        User_Media_Files = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures', is_active=True).order_by('-updated_on').first()
        # User_Media_Files = MediaFiles.objects.filter(updated_by=request.user).first()
        media_form = UpdateMediaForm(request.POST, request.FILES, instance=User_Media_Files)
        

        if user_form.is_valid() and profile_form.is_valid() and media_form.is_valid():
            user_form.save()
            profile_form.save()
            media_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('user_profile')  # Replace 'users-profile' with the appropriate URL name for your profile page
    else:
        user_form = UpdateUserForm(instance=request.user)
        Profile = UserProfile.objects.filter(user_id=request.user).first()
        profile_form = UpdateProfileForm(instance=Profile)
        User_Media_Files = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures', is_active=True).order_by('-updated_on').first()
        # User_Media_Files = MediaFiles.objects.filter(updated_by=request.user).first()
      
        media_form = UpdateMediaForm(request.POST, request.FILES, instance=User_Media_Files)

    context = {"head_title": "User Profile | Priority Gold Plus", 'user_form': user_form, 'profile_form': profile_form, 'media_form':media_form, 'user_media_instance':User_Media_Files}
    return render(request, 'account/user_profile.html', context)

@login_required
def edit_profile(request):
    # Check if the user has a profile instance
    try:
        profile_instance = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile_instance = None

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=profile_instance)
        User_Media_Files = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures').order_by('-updated_on').first()
        media_form = UpdateMediaForm(request.POST, request.FILES, instance=User_Media_Files)

        if profile_form.is_valid() and media_form.is_valid():
            media_instance = media_form.save(commit=False)
            media_instance.file_type = 'Profile Pictures'
            media_instance.is_active = True
            media_instance.updated_by = request.user
            media_instance.updated_on = timezone.now()
            media_instance.save()

            media_instance = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures').order_by('-updated_on').first()

            if profile_instance:
                # Update the existing profile instance
                profile_instance.profile_pic = media_instance.media_file
                profile_instance.updated_by = request.user
                profile_instance.updated_on = timezone.now()
                profile_instance.save()
            else:
                # Create a new profile instance for the user
                profile_instance = profile_form.save(commit=False)
                profile_instance.user = request.user
                profile_instance.profile_pic = media_instance.media_file
                profile_instance.updated_by = request.user
                profile_instance.updated_on = timezone.now()
                profile_instance.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect('users:user_profile')  # Replace 'users-profile' with the appropriate URL name for your profile page
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=profile_instance)
        User_Media_Files = MediaFiles.objects.filter(updated_by=request.user, file_type='Profile Pictures').order_by('-updated_on').first()
        media_form = UpdateMediaForm(instance=User_Media_Files)

    context = {"head_title": "Edit User Profile | Priority Gold Plus", 'user_form': user_form, 'profile_form': profile_form, 'media_form': media_form, 'user_media_instance': User_Media_Files}
    return render(request, 'account/edit_profile.html', context)


@login_required    
# Registration view for staff
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.created_by = request.user.id
            model_instance.created_on = timezone.now()
            model_instance.updated_by = request.user.id
            model_instance.updated_on = timezone.now()
            model_instance.save()
            # form.save()            
            # Additional logic or redirect here
            user = form.cleaned_data.get('username')
            messages.success(request, 'User profile was updated for ' + user)
            return redirect('/')  # Redirect to a success page
        else:
            print('User profile Form is not valid')
            messages.error(request, 'Error Processing Your Request')
            context = {'form': form,"head_title": "User Profile | Priority Gold Plus"}
            return render(request, 'users/admin/edit_profile.html', context)
    else:
        form = StaffRegisterForm()
        context = {'form': form,"head_title": "User Profile | Priority Gold Plus"}
        # data = {'form': form,"head_title": "Registration | Priority Gold"}
        return render(request, 'users/admin/edit_profile.html', context)
        
@login_required
def portfolio(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Portfolio | Priority Gold Plus"}
    return render(request, "users/portfolio.html", context)

@login_required
def portfolio_main(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Portfolio Main | Priority Gold Plus"}
    return render(request, "users/portfolio_main.html", context)

@login_required
def add_metal_form(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Add Metal | Priority Gold Plus"}
    return render(request, "users/add_metal_form.html", context)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["username"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from users.models import Message
from users.forms import MessageForm

User = get_user_model()

@user_passes_test(lambda u: u.is_superuser)
def send_mass_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            sender = request.user
            receivers = User.objects.filter(is_superuser=False)

            for receiver in receivers:
                message = Message.objects.create(sender=sender, receiver=receiver, content=content)
                # Add received message to user's profile
                receiver_profile = receiver.user_profile
                receiver_profile.received_messages.add(message)

            return redirect('admin:index')
    else:
        form = MessageForm()

    return render(request, 'admin_volt/send_mass_message.html', {'form': form})


from django.http import JsonResponse
from users.models import UserProfile
from portfolio.models import Portfolios, ProductPrices  
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, F
from django.db.models.functions import Coalesce
import json

from django.http import JsonResponse
from django.template.response import TemplateResponse

def chart_view(request, object_id):
    user_portfolios = Portfolios.objects.filter(
        created_by_id=object_id, is_deleted=False
    ).select_related("product", "metal", "grade")

    portfolio_data = []

    for portfolio in user_portfolios:
        product = portfolio.product
        metal = portfolio.metal
        grade = portfolio.grade

        # Calculate the acquisition value
        acquisition_value = portfolio.metal_value * portfolio.metal_quantity

        # Get the latest product price for the product
        latest_price = ProductPrices.objects.filter(
            sku=product.sku,
            metal_name=metal.metal_name,
            grade=grade.grade_name,
            is_active=True,
        ).latest("updated")

        # Calculate the current value
        current_value = (
            latest_price.ask * portfolio.metal_quantity * product.factor_rate
        )

        # Create a dictionary with portfolio data
        portfolio_entry = {
            "metal_name": metal.metal_name,
            "product_name": product.product_name,
            "metal_quantity": portfolio.metal_quantity,
            "acquisition_value": acquisition_value,
            "current_value": current_value,
        }

        portfolio_data.append(portfolio_entry)

    return JsonResponse({"portfolio_data": portfolio_data})

