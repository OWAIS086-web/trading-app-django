from django.shortcuts import render
from home.models import PrivacyPolicy, TermsAndCondition
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect


def home(request):
    packages = [
        {
            "name": "django-allauth",
            "url": "https://pypi.org/project/django-allauth/0.38.0/",
        },
        {
            "name": "django-bootstrap4",
            "url": "https://pypi.org/project/django-bootstrap4/0.0.7/",
        },
        {
            "name": "djangorestframework",
            "url": "https://pypi.org/project/djangorestframework/3.9.0/",
        },
    ]
    context = {"packages": packages}
    # ,{'head_title':'Home | Priority Gold'}
    return render(request, "home/index.html", context)
        
def about_us(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "About Us | Priority Gold Plus"}
    return render(request, "home/about_us.html", context)

def contact_us(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Contact Us | Priority Gold Plus"}
    return render(request, "home/contact_us.html", context)

def features(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Features | Priority Gold Plus"}
    return render(request, "home/features.html", context)

def careers(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Careers | Priority Gold Plus"}
    return render(request, "home/careers.html", context)
    
def daily_downloads(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Daily Downloads | Priority Gold", "page": page}
    context = {"head_title": "Daily Downloads | Priority Gold Plus"}
    return render(request, "home/daily_downloads.html", context)

def legal_framework(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Legal Framework | Priority Gold", "page": page}
    context = {"head_title": "Legal Framework | Priority Gold Plus"}
    return render(request, "home/legal_framework.html", context)

def the_exchange(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "The Exchange | Priority Gold", "page": page}
    context = {"head_title": "The Exchange | Priority Gold Plus"}
    return render(request, "home/the_exchange.html", context)

def market_summary(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Market Summary | Priority Gold", "page": page}
    context = {"head_title": "Market Summary | Priority Gold Plus"}
    return render(request, "home/market_summary.html", context)

def media_center(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Media Center | Priority Gold", "page": page}
    context = {"head_title": "Media Center | Priority Gold Plus"}
    return render(request, "home/media_center.html", context)


def page_privacy_policy(request):
    page = PrivacyPolicy.objects.first()
    data = {"head_title": "Privacy Policy | Priority Gold Plus", "page": page}
    # redirect_path = reverse("page-privacy-policy", data)
    # return HttpResponseRedirect(redirect_path)
    return render(request, "home/privacy_policy.html", data)


def page_terms_and_condition(request):
    page = TermsAndCondition.objects.first()
    data = {"head_title": "Terms & Conditions | Priority Gold Plus", "page": page}
    return render(request, "home/terms_and_conditions.html", data)


def page_about_us(request):
    # page = TermsAndCondition.objects.first()
    data = {
        "head_title": "About Us | Priority Gold Plus",
        # 'page': page
    }
    return render(request, "home/about.html", data)
