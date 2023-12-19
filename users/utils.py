from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_new_patient_user_email_confirmation(
    request, user, signup=True, email=None, password=None, implants=[]
):
    if not email:
        from allauth.account.utils import user_email

        email = user_email(user)
    if signup and not password:
        print("passwoord required")
    app_link_android = None
    app_link_ios = None
    from home.models import AppStoreLink

    try:
        app_store_links = AppStoreLink.objects.first()
    except AppStoreLink.DoesNotExist:
        app_store_links = None
    if app_store_links:
        app_link_android = app_store_links.google_play_store_link
        app_link_ios = app_store_links.apple_store_link

    from django.contrib.sites.models import Site

    try:
        current_site = Site.objects.get_current()
    except Site.DoesNotExist:
        current_site = None

    gs_bucket_name = settings.GS_BUCKET_NAME

    http_protocol = "http://"
    if request.is_secure():
        http_protocol = "https://"
    data = {
        "request": request,
        "current_site": current_site,
        "gs_bucket_name": gs_bucket_name,
        "user": user,
        "email": email,
        "password": password,
        "implants": implants,
        "http_protocol": http_protocol,
        "app_store_links": app_store_links,
        "app_link_android": app_link_android,
        "app_link_ios": app_link_ios,
    }
    html_message = render_to_string(
        "users/patients/emails/send_patient_signup_email.html", data
    )

    subject = "New Patient Account"
    from_email = f"Priority Gold <{settings.DEFAULT_FROM_EMAIL}>"
    message = ""
    recipient_list = [email]

    return send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=True,
    )


# myapp/utils.py
import requests
from .models import APIfetch

def fetch_users_from_api():
    url = "https://randomuser.me/api/?results=10"  # Fetching 10 random users (you can change the number as needed)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()['results']

        return data
    else:
        return None

def save_users_to_database():
    data = fetch_users_from_api()
    if data is not None:
        for user_data in data:
            user = APIfetch(
                fname=user_data['name']['first'],
                lname=user_data['name']['last'],
                email=user_data['email'],
                username=user_data['login']['username'],
                phone=user_data['phone'],
                date_of_birth=user_data['dob']['date'][:10],
                gender=user_data['gender'],
            )
            user.save()
