from django.urls import path
# from .views import home, page_privacy_policy, page_terms_and_condition,page_about_us
from . import views

app_name = "home"
urlpatterns = [
    path("", views.home, name="home"),
    path("about-us/", views.about_us, name="about_us"),    
    path("careers/", views.careers, name="careers"),
    path("daily-downloads/", views.daily_downloads, name="daily_downloads"),
    path("legal-framework/", views.legal_framework, name="legal_framework"),
    path("the-exchange/", views.the_exchange, name="the_exchange"),
    path("market-summary/", views.market_summary, name="market_summary"),
    path("media-center/", views.media_center, name="media_center"),
    path("privacy-policy/", views.page_privacy_policy, name="privacy_policy"),
    path("terms-and-conditions/", views.page_terms_and_condition, name="terms_and_condition"),
    path('contact-us/',views.contact_us,name='contact_us'), 
    path('features/',views.features,name='features'),
]
