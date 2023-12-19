from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, UserProfile,MediaFiles
from django.contrib.auth import get_user_model, forms as auth_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
User = get_user_model()

class UserRegisterForm(UserCreationForm,PopRequestMixin, CreateUpdateAjaxMixin,):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Re-Type Password'
    # username = forms.CharField(max_length=150, required = True, label='User Name', widget=forms.TextInput(attrs={'class': 'form-signup', 'placeholder': 'User Name'}),)
    email = forms.EmailField(max_length=254, required = True, 
                             label='Email Address', 
                             widget=forms.EmailInput(attrs={'class': 'form-signup', 'placeholder': 'example@domain.com'}),
                             )
    terms_of_services = forms.BooleanField(label="Terms Of Services",required=True,widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)

    class Meta:
        model = User
        fields = ['email','password1','password2','terms_of_services',]

class StaffRegisterForm(UserCreationForm,PopRequestMixin, CreateUpdateAjaxMixin,):
    # username = forms.CharField(max_length=150, required = True, label='User Name', widget=forms.TextInput(attrs={'class': 'form-signup', 'placeholder': 'User Name'}),)
    email = forms.EmailField(max_length=254, required = True, 
                             label='Email Address', 
                             widget=forms.EmailInput(attrs={'class': 'form-signup', 'placeholder': 'example@domain.com'}),
                             )
    is_staff = forms.BooleanField(label="Is Staff?",required=True,widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)
    terms_of_services = forms.BooleanField(label="Terms Of Services",required=True,widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)

    class Meta:
        model = User
        fields = ['email','username','password1','password2','is_staff','terms_of_services',]

class AdminRegisterForm(UserCreationForm,PopRequestMixin, CreateUpdateAjaxMixin,):
    # username = forms.CharField(max_length=150, required = True, label='User Name', widget=forms.TextInput(attrs={'class': 'form-signup', 'placeholder': 'User Name'}),)
    email = forms.EmailField(max_length=254, required = True, 
                             label='Email Address', 
                             widget=forms.EmailInput(attrs={'class': 'form-signup', 'placeholder': 'example@domain.com'}),
                             )    
    is_staff = forms.BooleanField(label="Is Staff?",widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)
    is_admin = forms.BooleanField(label="Is Admin?",widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)
    terms_of_services = forms.BooleanField(label="Terms Of Services",required=True,widget=forms.CheckboxInput(attrs={'class': 'checkbox-signup'}),)

    class Meta:
        model = User
        fields = ['email','username','password1','password2','is_staff','is_admin','terms_of_services',]


class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ['prefix','first_name','middle_name', 'last_name','display_name','biography','profile_pic',
                  'telephone','cell','fax','website','twitter','skype','linkedin','facebook','instagram',
                  'unit','street','country','region','city','instagram','postal_code']
        labels = {'prefix': 'Prefix', 'first_name': 'First Name','middle_name': 'Middle Name', 'last_name': 'Last Name',
            'display_name': 'User Display Name',
            'biography': 'Biography',
            'profile_pic': 'Profile Picture',
            'telephone': 'Telephone',
            'cell': 'Cell',
            'fax': 'Fax',
            'website': 'Website',
            'twitter': 'Twitter',
            'skype': 'Skype',
            'linkedin': 'LinkedIn',
            'facebook': 'Facebook',
            'instagram': 'Instagram',
            'unit': 'Unit',
            'street': 'Street',
            'country': 'Country',
            'region': 'Region',
            'city': 'City',
            'postal_code': 'Postal Code',
        }
        placeholders = {
            'telephone':'+999999999','cell':'+999999999','fax':'+999999999',
            'website':'www.domain.com','twitter':'Twitter','skype':'Skype','linkedin':'LinkedIn','facebook':'Facebook','instagram':'Instagram',
            'unit':'Unit #','street':'Street','postal_code':'Postal Code',
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['prefix'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['middle_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['display_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['biography'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone'].widget.attrs.update({'class': 'form-control'})
        self.fields['cell'].widget.attrs.update({'class': 'form-control'})
        self.fields['fax'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['twitter'].widget.attrs.update({'class': 'form-control'})
        self.fields['skype'].widget.attrs.update({'class': 'form-control'})
        self.fields['linkedin'].widget.attrs.update({'class': 'form-control'})
        self.fields['facebook'].widget.attrs.update({'class': 'form-control'})
        self.fields['instagram'].widget.attrs.update({'class': 'form-control'})
        self.fields['unit'].widget.attrs.update({'class': 'form-control'})
        self.fields['street'].widget.attrs.update({'class': 'form-control'})
        self.fields['country'].widget.attrs.update({'class': 'form-control'})
        self.fields['region'].widget.attrs.update({'class': 'form-control'})
        self.fields['city'].widget.attrs.update({'class': 'form-control'})
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control'})


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    id = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))
    is_active = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    # otp = forms.CharField(max_length=6, required=False , default='')
    class Meta:
        model = User
        fields = ['username', 'email','is_active']


class UpdateProfileForm(forms.ModelForm):
    display_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Display Name', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    profile_pic = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file', 'id':'profile-picture-upload'}))

    biography = forms.CharField(max_length=1024,required=False, widget=forms.Textarea(attrs={'placeholder': 'Strategy', 'class': 'form-control', 'rows': 15}))
    telephone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'}))
    street = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control'}))


    class Meta:
        model = UserProfile
        fields = ['profile_pic','display_name','first_name','last_name', 'biography','street','telephone']

class UpdateMediaForm(forms.ModelForm):   
    file_type = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'File Type', 'class': 'form-control'}))
    title = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    # media_file = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file', 'id':'media-file-upload'}))
    media_file = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'form-control-file', 'id':'media-file-upload'}))
    description = forms.CharField(max_length=1024,required=False, widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control', 'rows': 5}))
    is_active = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = MediaFiles
        fields = ['file_type','title','media_file','description', 'is_active']


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(auth_forms.UserCreationForm):
    error_message = auth_forms.UserCreationForm.error_messages.update(
        {"duplicate_email": _("This email has already been register.")}
        # {"duplicate_email": _("This username has already been taken.")}
    )

    class Meta(auth_forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        email = self.cleaned_data["email"]

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email

        raise ValidationError(self.error_messages["duplicate_email"])


from django import forms
from django.contrib.admin.helpers import ActionForm

class SendMessageForm(ActionForm):
    message = forms.CharField(widget=forms.Textarea)


from django import forms

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))

    def clean_content(self):
        content = self.cleaned_data['content']
        if not content.strip():
            raise forms.ValidationError("Message content cannot be empty.")
        return content