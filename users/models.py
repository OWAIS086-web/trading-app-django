from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone
from cities_light.models import Country, Region, City
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from subscriptions.models import Subscription
from PIL import Image
from django.db import models
from django.conf import settings
class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # ... other fields and methods ...

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} - {self.timestamp}"






class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_admin', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)        
        extra_fields.setdefault('is_locked_out', False)
        extra_fields.setdefault('is_deleted', False)
        return self.create_user(email, password, **extra_fields)

    def create_admin(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)        
        extra_fields.setdefault('is_locked_out', False)
        extra_fields.setdefault('is_deleted', False)
        return self.create_user(email, password, **extra_fields)
        
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_approved', True)        
        extra_fields.setdefault('is_locked_out', False)
        extra_fields.setdefault('is_deleted', False)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_("User Name"), blank=True, null=True, max_length=150)
    email = models.EmailField(_("Email Address"), default='email@mydomain.cm', blank=False, null=False, max_length=254,unique=True)
    USERNAME_FIELD = 'email' #username

    is_active = models.BooleanField(_("Is Active?"), null=False,default=False) #can login
    is_approved = models.BooleanField(_("Is Approved?"), null=False,default=True) #can login
    is_locked_out = models.BooleanField(_("Is Locked Out?"), null=False,default=False) #cant login
    is_deleted = models.BooleanField(_("Is Deleted?"), null=False,default=False)
    is_superuser = models.BooleanField(_("Is Super User?"), null=False,default=False)
    is_admin = models.BooleanField(_("Is Admin?"), null=False,default=False)
    is_staff = models.BooleanField(_("Is Staff?"), null=False,default=False)
    date_joined = models.DateTimeField(_("Joining Date"), auto_now_add=True, blank=False, null=False)
    last_ipaddress = models.CharField(_("Last IP Address"), blank=True, null=True, max_length=30)
    last_login = models.DateTimeField(_("Last Login Date"), blank=True, null=True)
    last_password_changed_date = models.DateTimeField(_("Last Password Changed Date"), blank=True, null=True)
    last_lockout_date = models.DateTimeField(_("Last Lockout Date"), blank=True, null=True)
    last_activity_date = models.DateTimeField(_("Last Activity Date"), blank=True, null=True)
    failed_password_attempt_count = models.IntegerField(_("Failed Password Attempt Count"), default=0, blank=False, null=False) 
    notifications = models.BooleanField(_("Notifications"), default=True)
    terms_of_services = models.BooleanField(_("Terms Of Services"),default=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_users', verbose_name=_("Created By"))
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_users', verbose_name=_("Updated By"))
    updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)    
    

    REQUIRED_FIELDS=[] #'first_name','email',

    objects = UserManager()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        if self.email:
            return f"{self.email}"
        return "%s" % self.username

    class Meta:
        verbose_name_plural = _("List of all Users")
    

    @property
    def get_subscription(self):
        try:
            return self.subscription
        except Subscription.DoesNotExist:
            return None

    @property
    def get_active_subscription(self):
        try:
            return self.subscription
        except Subscription.DoesNotExist:
            return None
        # return self.pk

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE, default=None)
    signup_source = models.CharField(default='unknown ',max_length=50) 
    received_messages = models.ManyToManyField(Message, related_name='received_by_user', blank=True)
    display_name = models.CharField(_("User Display Name"), blank=True, null=True, max_length=254)
    prefix = models.CharField(_("Prefix"), default='prefix', blank=True, null=True, max_length=10)
    first_name = models.CharField(_("First Name"), default='first name', blank=True, null=True, max_length=100)
    middle_name = models.CharField(_("Middle Name"), blank=True, null=True, max_length=100)
    last_name = models.CharField(_("Last Name"), blank=True, null=True, max_length=100) 
    biography = models.CharField(_("Biography"), blank=True, null=True, max_length=1024)
    profile_pic = models.ImageField(default="profile.png", null=True, blank=True, upload_to='profile_images')

    # phone_regex = RegexValidator(
    #     regex=r'^\+?1?\d{9,15}$',
    #     message="Telephone must be entered in the format: '+999999999'. Up to 15 digits allowed."
    # )
    telephone = models.CharField(_("Telephone"), max_length=20, blank=True, null=True)

    cell_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Cell must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    cell = models.CharField(_("Cell"),validators=[cell_regex], max_length=20, blank=True, null=True)
    
    fax_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Fax must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    fax = models.CharField(_("Fax"),validators=[fax_regex], max_length=20, blank=True, null=True)

    website = models.CharField(_("Website"), blank=True, null=True, max_length=254) 
    twitter = models.CharField(_("Twitter"), blank=True, null=True, max_length=254) 
    skype = models.CharField(_("Skype"), blank=True, null=True, max_length=254) 
    linkedin = models.CharField(_("LinkedIn"), blank=True, null=True, max_length=254) 
    facebook = models.CharField(_("Facebook"), blank=True, null=True, max_length=254) 
    instagram = models.CharField(_("Instagram"), blank=True, null=True, max_length=254) 

    unit = models.CharField(_("Unit"), null=True,max_length=10)
    street = models.CharField(_("Street"), null=True,max_length=50)
    country = models.ForeignKey(Country, null=True,on_delete=models.CASCADE, verbose_name=_("Country"))
    region = models.ForeignKey(Region, null=True,on_delete=models.CASCADE, verbose_name=_("State"))
    city = models.ForeignKey(City, null=True,on_delete=models.CASCADE, verbose_name=_("City"))
    
    postal_code = models.CharField(_("Postal Code"), null=True,max_length=25)

    otp = models.CharField(_("OTP"), null=True, max_length=6)
    otp_expiry_time = models.DateTimeField(_("OTP Expiry Time"),default=timezone.now,null=True, blank=True) 

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=False, related_name='created_user_profile', verbose_name=_("Created By"))
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=False, related_name='updated_user_profile', verbose_name=_("Updated By"))
    updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)    

    def __str__(self):
        return self.user.email
    
    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.profile_pic.path)    


FILE_TYPE_PROFILE_PIC = 'Profile Pictures'
FILE_TYPE_USER_DOC = 'User Documents'
FILE_TYPE_COMPANY_DOC = 'Company Documents'

FILE_TYPE_CHOICES = (
    (FILE_TYPE_PROFILE_PIC, _('Profile Pictures')),
    (FILE_TYPE_USER_DOC, _('User Documents')),
    (FILE_TYPE_COMPANY_DOC, _('Company Documents')),
    )
def get_absolute_url(self):
        return reverse("admin:profile_change", args=[str(self.id)])
    

from django.db import models
from .models import UserProfile 

class UserProduct(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    # Add other fields as needed

    def __str__(self):
        return self.product_name


class MediaFiles(models.Model):
    # media_file = models.ImageField(_("Media File"),default="default.png", null=True, blank=True, upload_to='media')
    media_file= models.FileField(default="profile.png", null=True, blank=True, upload_to='media')
    title = models.CharField(_("Title"), null=True,max_length=50)
    file_type = models.CharField(_("File Type"), choices=FILE_TYPE_CHOICES, max_length=50, null=True, blank=True)
    # uploaded_at = models.DateTimeField(auto_now_add=True)
    # user = models.OneToOneField(User, related_name='user_media', on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)            
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey for the User
    description = models.CharField(_("Description"), blank=True, null=True, max_length=1024)
    is_active = models.BooleanField(_("Is Active?"), null=False,default=False)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, editable=False, related_name='updated_media_files', verbose_name=_("Updated By"))
    updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return self.title



class APIfetch(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField()
    username = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    updated_on = models.DateTimeField(auto_now=True)
    time = models.TimeField(default='00:00:00')
    time_fetching = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    created_by = models.CharField(max_length=100)
    category = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.fname} {self.lname}"



# models.py


class TrafficData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField()
    device_type = models.CharField(max_length=50)

