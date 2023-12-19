from django.shortcuts import render, redirect
from admin_volt.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserPasswordChangeForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.contrib.auth import logout
from django.db.models import Count
from users.models import User
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from admin_volt.utils import JsonResponse
from django.contrib.auth.decorators import login_required
import json
# Index



  

# Dashboard
def dashboard(request):
  context = {
    'segment': 'dashboard'
  }
  return render(request, 'pages/dashboard/dashboard.html', context)

# Pages
@login_required(login_url="/accounts/login/")
def transaction(request):
  context = {
    'segment': 'transactions'
  }
  return render(request, 'pages/transactions.html', context)

@login_required(login_url="/accounts/login/")
def settings(request):
  context = {
    'segment': 'settings'
  }
  return render(request, 'pages/settings.html', context)

# Tables
@login_required(login_url="/accounts/login/")
def bs_tables(request):
  context = {
    'parent': 'tables',
    'segment': 'bs_tables',
  }
  return render(request, 'pages/tables/bootstrap-tables.html', context)

# Components
@login_required(login_url="/accounts/login/")
def buttons(request):
  context = {
    'parent': 'components',
    'segment': 'buttons',
  }
  return render(request, 'pages/components/buttons.html', context)

@login_required(login_url="/accounts/login/")
def notifications(request):
  context = {
    'parent': 'components',
    'segment': 'notifications',
  }
  return render(request, 'pages/components/notifications.html', context)

@login_required(login_url="/accounts/login/")
def forms(request):
  context = {
    'parent': 'components',
    'segment': 'forms',
  }
  return render(request, 'pages/components/forms.html', context)

@login_required(login_url="/accounts/login/")
def modals(request):
  context = {
    'parent': 'components',
    'segment': 'modals',
  }
  return render(request, 'pages/components/modals.html', context)

@login_required(login_url="/accounts/login/")
def typography(request):
  context = {
    'parent': 'components',
    'segment': 'typography',
  }
  return render(request, 'pages/components/typography.html', context)


# Authentication
def register_view(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      print("Account created successfully!")
      form.save()
      return redirect('/accounts/login/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = { 'form': form }
  return render(request, 'accounts/sign-up.html', context)

class UserLoginView(LoginView):
  form_class = LoginForm
  template_name = 'accounts/sign-in.html'

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password-change.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/forgot-password.html'
  form_class = UserPasswordResetForm

class UserPasswrodResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/reset-password.html'
  form_class = UserSetPasswordForm

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

def lock(request):
  return render(request, 'accounts/lock.html')

# Errors
def error_404(request):
  return render(request, 'pages/examples/404.html')

def error_500(request):
  return render(request, 'pages/examples/500.html')

# Extra
def upgrade_to_pro(request):
  return render(request, 'pages/upgrade-to-pro.html')

  def user_counts(request):
    user_data = APIfetch.objects.all()

    data = []
    for user in user_data:
      data.append({
        'fname': user.fname,
        'lname': user.lname,
        'count': user.time_fetching,
      })

    return JsonResponse({'data': data})
  
def password_change_done(request):
    return redirect('settings') 


# this view function take user from db according to condition 
from django.utils import timezone
from users.models import User

def user_chart_view(request):
    today = timezone.now()

    one_week_ago = today - timezone.timedelta(weeks=1)
    one_month_ago = today - timezone.timedelta(days=30)
    one_year_ago = today - timezone.timedelta(days=365)

    total_users_today = User.objects.filter(created_on__gte=today - timezone.timedelta(hours=24)).count()
    total_users_week = User.objects.filter(created_on__gte=one_week_ago).count()
    total_users_month = User.objects.filter(created_on__gte=one_month_ago).count()
    total_users_year = User.objects.filter(created_on__gte=one_year_ago).count()

    context = {
        'total_users_today': total_users_today,
        'total_users_week': total_users_week,
        'total_users_month': total_users_month,
        'total_users_year': total_users_year,
    }

    return render(request, 'admin/index.html', context)
  

# this view function take session data  from db  to show login user information 
from django.contrib.sessions.models import Session
from users.models import User
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render

from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.utils import timezone

def logged_in_users(request):
    current_time = timezone.now()
    active_sessions = Session.objects.filter(expire_date__gte=current_time)

    users_data = []
    for session in active_sessions:
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        username = None
        
        # Check if '_auth_user_username' exists in the session data
        if '_auth_user_username' in session_data:
            username = session.get_decoded().get('_auth_user_username')

        
        data = {
            'session_key': session.session_key,
            'user_id': user_id,
            'username': username
        }
        users_data.append(data)

    return JsonResponse({'logged_in_users': users_data})
  

from collections import defaultdict
from django.db.models import Sum
from django.http import JsonResponse
from user_agents import parse
from users.models import TrafficData

def determine_device_type(user_agent_string):
    user_agent = parse(user_agent_string)
    if user_agent.is_mobile:
        return "Mobile"
    elif user_agent.is_tablet:
        return "Tablet"
    elif user_agent.is_pc:
        return "Desktop / Laptop"
    else:
        return "Unknown"

def update_traffic_data(device_type):
    try:
        TrafficData.objects.create(count=1, device_type=device_type)
    except Exception as e:
        # Handle database insertion errors here, e.g., log the error
        pass

def chart(request):
    user_agent_string = request.META.get('HTTP_USER_AGENT', '')
    device_type = determine_device_type(user_agent_string)
    update_traffic_data(device_type)
    return JsonResponse({'message': 'Traffic data updated successfully'})

def get_traffic_data(request):
    all_device_types = ['Mobile', 'Tablet', 'Desktop / Laptop']
    device_traffic_data = TrafficData.objects.values('device_type').annotate(total_count=Sum('count'))
    
    device_counts = defaultdict(int)
    for entry in device_traffic_data:
        device_counts[entry['device_type']] = entry['total_count']
    
    device_types = all_device_types
    device_counts = [device_counts[device_type] for device_type in all_device_types]
    
    return JsonResponse({'device_types': device_types, 'device_counts': device_counts})



from django.http import JsonResponse
from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialApp, SocialAccount

def get_social_account_data(request):
    # Get the SocialApp objects for the desired providers
    social_apps = SocialApp.objects.filter(provider__in=['apple', 'google', 'facebook'])

    # Initialize counts for each provider to zero
    provider_counts = {'apple': 0, 'google': 0, 'facebook': 0, 'email': 0}

    # Loop through SocialApp objects and count associated SocialAccount instances
    for social_app in social_apps:
        provider = social_app.provider
        count = SocialAccount.objects.filter(provider=provider).count()
        provider_counts[provider] = count

    # Fetch the count of users who signed up using their email address
    email_count = EmailAddress.objects.filter(verified=True).count()
    provider_counts['email'] = email_count

    # Prepare data for the chart
    labels = list(provider_counts.keys())
    counts = list(provider_counts.values())

    data = {'labels': labels, 'counts': counts}
    return JsonResponse(data)


