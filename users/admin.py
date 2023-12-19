from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe

from admin_volt import forms
from modules.admin_mixin import AdminMediaMixin
from users.forms import UserRegisterForm, StaffRegisterForm, AdminRegisterForm, UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(AdminMediaMixin, UserAdmin):
    form = UserChangeForm
    add_form = AdminRegisterForm
    fieldsets = (
                    ("User",
                     {"fields": (
                         'failed_password_attempt_count', 'last_password_changed_date', 'profile_pic',
                         'created_by', 'created_on', 'updated_by', 'updated_on'
                     )}),
                ) + UserAdmin.fieldsets

    list_display = [
        "display_user_first_column",
        # "username",
        "email",
        "password",
        'is_admin', 'is_approved', 'is_deleted', 'is_locked_out', 'last_lockout_date', 'terms_of_services',
        'last_login', 'last_ipaddress', 'last_activity_date', 'failed_password_attempt_count',
        'last_password_changed_date',
        'created_by',
        # 'get_created_by',
        'created_on',
        'updated_by',
        # 'get_updated_by',
        'updated_on',
        # "get_country",
        # "user_type",
        "get_button_actions",
        "date_joined",
    ]
    search_fields = ["username", "email"]
    # list_select_related = ["doctor_profile", "patient_profile"]
    readonly_fields = (
    'last_login', 'last_ipaddress', 'last_activity_date', 'failed_password_attempt_count', 'last_password_changed_date',
    'created_by', 'created_on', 'updated_by', 'updated_on')
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    # "username",
                    "email",
                    'is_staff', 'is_admin', 'is_superuser',
                    'is_active', 'is_approved',
                    # 'is_deleted','is_locked_out','last_lockout_date',
                    'terms_of_services',
                    # 'last_login','last_ipaddress','last_activity_date',
                    # 'failed_password_attempt_count','last_password_changed_date',
                    # "isanonymous",
                    # "isapproved",
                    # "issuperuser",
                    # "isadmin",
                    # "isstaff",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    @admin.display(description="Created By")
    def get_created_by(self, instance):
        # Retrieve the users by their IDs
        users = User.objects.filter(id__in=instance.created_by)
        for user in users:
            return user.email

    @admin.display(description="Updated By")
    def get_updated_by(self, instance):
        # Retrieve the users by their IDs
        users = User.objects.filter(id__in=instance.updated_by)
        for user in users:
            return user.email

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        model_name = request.GET.get("model_name", None)
        if model_name == "doctorprofile":
            queryset, use_distinct = super().get_search_results(
                request, queryset.filter(user_type=User.USER_TYPE_DOCTOR), search_term
            )
            return queryset, use_distinct
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        return queryset, use_distinct

    @admin.display(description="Email", ordering="email")
    def display_user_first_column(self, instance):
        if instance.email:
            return "%s" % instance.email
        return "%s" % instance.email

    # @admin.display(description="Country")
    # def get_country(self, instance):
    #     if instance.user_type == User.USER_TYPE_DOCTOR and instance.doctor_profile:
    #         return instance.doctor_profile.country
    #     elif instance.user_type == User.USER_TYPE_PATIENT and instance.patient_profile:
    #         return instance.patient_profile.country
    #     else:
    #         return None

    def get_object_by_id(self, object_id):
        try:
            # user = User.objects.select_related("doctor_profile").get(id=object_id)
            user = User.objects.get(id=object_id)
        except User.DoesNotExist:
            user = None
        return user

    @admin.display(description="Actions")
    def get_button_actions(self, instance):
        html = f'<a href="{instance.id}/profile/" class="btn-admin-primary">View</a>'
        return mark_safe(html)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/profile/",
                self.admin_site.admin_view(self.user_profile_view),
                name="user_profile_view",
            ),
        ]
        return custom_urls + urls

    def user_profile_view(self, request, object_id):
        user = self.get_object_by_id(object_id=object_id)
        context = dict(
            self.admin_site.each_context(request),
            user=user,
            title=f"{user}",
        )
        return render(request, "users/admin/user_detail.html", context)

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.template.response import TemplateResponse
from django.urls import path
from .models import UserProfile, UserProduct
from portfolio.models import Portfolios, ProductPrices
from django.contrib.auth.decorators import login_required
from decimal import Decimal

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'display_name', 'telephone', 'cell', 'city', 'country', 'profile_pic_display', 'view_button', 'edit_button', 'delete_button', 'chart_button')  # Add 'chart_button' to the list display
    list_filter = ('country', 'city')
    search_fields = ('user__email', 'display_name', 'telephone', 'cell')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def profile_pic_display(self, obj):
        if obj.profile_pic:
            img_html = '<img class="profile-pic" src="{}" width="50" height="50" style="border-radius: 50%;" data-image="{}" />'.format(obj.profile_pic.url, obj.profile_pic.url)
            return format_html('<div class="profile-pic-container">{}</div>'.format(img_html))
        else:
            return 'No Image'
    profile_pic_display.short_description = 'Profile Picture'

    def view_button(self, obj):
        return format_html('<a href="{}" class="round-button view-button" target="_blank">View</a>', reverse('admin:users_userprofile_change', args=[obj.id]))
    view_button.short_description = 'View'

    def edit_button(self, obj):
        return format_html('<a href="{}" class="round-button edit-button">Edit</a>', reverse('admin:users_userprofile_change', args=[obj.id]))
    edit_button.short_description = 'Edit'

    def delete_button(self, obj):
        return format_html('<a href="{}" class="round-button delete-button" onclick="return confirm(\'Are you sure you want to delete this profile?\')">Delete</a>', reverse('admin:users_userprofile_delete', args=[obj.id]))
    delete_button.short_description = 'Delete'

    def chart_button(self, obj):
        chart_url = reverse('admin:userprofile-chart', args=[obj.id])
        return format_html('<a href="{}" class="round-button chart-button rose-gold">Chart</a>', chart_url)

    chart_button.short_description = 'Chart'

    def chart_view(self, request, object_id):
        user_profile = UserProfile.objects.get(pk=object_id)

        # Retrieve the user's portfolios
        user_portfolios = Portfolios.objects.filter(created_by=user_profile.user, is_deleted=False)
        portfolio_data = []

        for portfolio in user_portfolios:
            product = portfolio.product
            metal = portfolio.metal
            grade = portfolio.grade

            # Calculate the acquisition value
           # Ensure that all variables are of type decimal.Decimal
            portfolio_metal_value = Decimal(str(portfolio.metal_value))
            portfolio_metal_quantity = Decimal(str(portfolio.metal_quantity))

            # Calculate the acquisition value
            acquisition_value = portfolio_metal_value * portfolio_metal_quantity

            # Get the latest product price for the product
            latest_price = ProductPrices.objects.filter(
                sku=product.sku, metal_name=metal.metal_name, grade=grade.grade_name, is_active=True
            ).latest('updated')

            # Calculate the current value
            # Ensure that all variables are of type decimal.Decimal
            latest_price_ask = Decimal(str(latest_price.ask))
            portfolio_metal_quantity = Decimal(str(portfolio.metal_quantity))
            product_factor_rate = Decimal(str(product.factor_rate))

            # Calculate the current value
            current_value = latest_price_ask * portfolio_metal_quantity * product_factor_rate

            # Create a dictionary with portfolio data
            portfolio_entry = {
                'metal_name': metal.metal_name,
                'product_name': product.product_name,
                'metal_quantity': portfolio.metal_quantity,
                'acquisition_value': acquisition_value,
                'current_value': current_value,
            }

            portfolio_data.append(portfolio_entry)

        # Calculate total values
        total_acquisition_value = sum(entry['acquisition_value'] for entry in portfolio_data)
        total_current_value = sum(entry['current_value'] for entry in portfolio_data)

        # Determine if it's a profit or loss based on the total values
        profit_loss_flag = "Profit" if total_current_value > total_acquisition_value else "Loss"

        # Create a dictionary with user and portfolio data
        user_portfolio_data = {
            'user_id': user_profile.user.id,
            'user_username': user_profile.user.username,
            'display_name': user_profile.display_name,
            'user_email': user_profile.user.email,
            'total_acquisition_value': total_acquisition_value,
            'total_current_value': total_current_value,
            'profit_loss_flag': profit_loss_flag,
            'portfolio_data': portfolio_data,
        }
        labels = [entry['product_name'] for entry in portfolio_data]
       
        # Convert Decimal objects to float values for acquisitionValues
        acquisitionValues = [float(entry['acquisition_value']) for entry in portfolio_data]

        context = {
            'user_profile': user_profile,
            'user_portfolio_data': user_portfolio_data,
            'labels': labels, 
            'acquisitionValues': acquisitionValues,
        }

        # Render the chart using a template
        return TemplateResponse(request, "admin/userprofile_chart.html", context)
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/chart/',  # Change '<id>' to '<path:object_id>'
                self.admin_site.admin_view(self.chart_view),
                name='userprofile-chart',
            ),
        ]
        return custom_urls + urls

    class Media:
        css = {
            'all': ('css/admin_buttons.css',),  # Include the path to your custom CSS file
        }
        js = ('js/profile_pic_hover.js',)  # Include the path to your custom JavaScript file

admin.site.register(UserProfile, UserProfileAdmin)


