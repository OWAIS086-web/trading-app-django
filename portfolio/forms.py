from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import *


GRADE_BU = 'BU'
GRADE_BULLION = 'Bullion'
GRADE_CIRC = 'Circ'
GRADE_PRE_1933_US_GOLD_COINS = 'pre-1933 US Gold Coins'
GRADE_PROOF = 'Proof'

GRADE_CHOICES = (
    (GRADE_BU, _('BU')),
    (GRADE_BULLION, _('Bullion')),
    (GRADE_CIRC, _('Circ')),
    (GRADE_PRE_1933_US_GOLD_COINS, _('pre-1933 US Gold Coins')),
    (GRADE_PROOF, _('Proof')),
    )


STATUS_IN_STOCK = 0

STATUS_1_2_WEEK_DELAY = 1
STATUS_2_3_WEEK_DELAY = 2
STATUS_3_4_WEEK_DELAY = 3
STATUS_4_5_WEEK_DELAY = 4
STATUS_5_6_WEEK_DELAY = 5
STATUS_6_7_WEEK_DELAY = 6
STATUS_7_8_WEEK_DELAY = 7
STATUS_8_9_WEEK_DELAY = 8
STATUS_OUT_OF_STOCK = 9
STATUS_UNAVAILABLE = 10

PRODUCT_STATUS_CHOICES = (
    (STATUS_1_2_WEEK_DELAY, '1-2 Week Delay'),
    (STATUS_2_3_WEEK_DELAY, '2-3 Week Delay'),
    (STATUS_3_4_WEEK_DELAY, '3-4 Week Delay'),
    (STATUS_4_5_WEEK_DELAY, '4-5 Week Delay'),
    (STATUS_5_6_WEEK_DELAY, '5-6 Week Delay'),
    (STATUS_IN_STOCK, 'In Stock'),
    (STATUS_OUT_OF_STOCK, 'Out Of Stock'),
    (STATUS_UNAVAILABLE, 'Unavailable'),
)

SHIPPING_STATUS_CHOICES = (
    (STATUS_1_2_WEEK_DELAY, '1-2 Week Delay'),
    (STATUS_2_3_WEEK_DELAY, '2-3 Week Delay'),
    (STATUS_3_4_WEEK_DELAY, '3-4 Week Delay'),
    (STATUS_4_5_WEEK_DELAY, '4-5 Week Delay'),
    (STATUS_5_6_WEEK_DELAY, '5-6 Week Delay'),
    (STATUS_6_7_WEEK_DELAY, '6-7 Week Delay'),
    (STATUS_7_8_WEEK_DELAY, '7-8 Week Delay'),
    (STATUS_8_9_WEEK_DELAY, '8-9 Week Delay'),
    #(STATUS_IN_STOCK, 'In Stock'),
    (STATUS_OUT_OF_STOCK, 'Out Of Stock'),
    #(STATUS_UNAVAILABLE, 'Unavailable'),
)


class ReadOnlyDecimalField(forms.DecimalField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.attrs['readonly'] = True  # Set the field as read-only

# class PortfolioForm(forms.ModelForm):   
#     metal = forms.ModelChoiceField(queryset=Metals.objects.filter(is_active=True).order_by('metal_name'),
#         widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'metalChange()'}), label='Metal', required=True,
#         to_field_name='metal_id',  # Set the custom column as the value to use
#         )
        
#     grade = forms.ModelChoiceField(queryset=Grades.objects.filter(is_active=True).order_by('grade_name'),
#         widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'metalChange()'}), label='Grade', required=True)
          
#     product_family = forms.ModelChoiceField(queryset=ProductFamilies.objects.filter(is_active=True).order_by('productfamily_name'),
#         widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'getProducts()'}), label='Product Family', required=True,
#         to_field_name='productfamily_id',  # Set the custom column as the value to use
#     )

#     product = forms.ModelChoiceField(queryset=Products.objects.filter(is_active=True).order_by('product_name'),
#         widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'setOuncesValue()'}), label='Product', required=True)
    
#     ounces = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control' 'form-control-ounces'}), label='Ounces', initial='0.0000', required=True )
    
#     metal_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Quantity',
#                                   initial='0',  # Set the default value here 
#                                   required=True)
    
#     acquisition_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Acquisition Cost',
#                                   initial='0.0000',  # Set the default value here 
#                                   required=True)
    
#     purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'datepicker'}), label='Purchase Date',
#                                     required=True, initial=timezone.now()  # Set default value to the current date and time // ,help_text='Select the purchase date'
#                                     )

#     def clean_metal_quantity(self):
#         metal_quantity = self.cleaned_data.get('metal_quantity')
#         if metal_quantity <= 0:
#             raise forms.ValidationError("Metal quantity must be greater than zero.")
#         return metal_quantity

#     def clean_acquisition_cost(self):
#         acquisition_cost = self.cleaned_data.get('acquisition_cost')
#         if acquisition_cost <= 0:
#             raise forms.ValidationError("Acquisition cost must be greater than zero.")
#         return acquisition_cost

#     def clean_purchase_date(self):
#         purchase_date = self.cleaned_data.get('purchase_date')
#         current_date = timezone.now().date()

#         if purchase_date > current_date:
#             raise forms.ValidationError("Purchase date cannot be in the future.")
#         return purchase_date


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['product'].queryset = Products.objects.filter(is_active=True).order_by('product_name')

#         # Attach related metal to each product family option
#         for obj in self.fields['product'].queryset:
#             product_family = obj.product_family
#             metal = obj.metal
#             obj.label = f'{obj.product_name} ({product_family.productfamily_name}) ({metal.metal_name})'
#             obj.metal_id = metal.id  # Set a custom attribute for the metal ID
#             obj.productfamily_id = product_family.productfamily_id  # Set a custom attribute for the metal ID


#     class Meta:
#         model = Portfolios
#         fields = ['metal','product_family','grade','product','ounces','acquisition_cost','purchase_date']



class PortfolioForm(forms.ModelForm):   
    metal = forms.ModelChoiceField(queryset=Metals.objects.filter(is_active=True).order_by('metal_name'),
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'metalChange()'}), label='Metal', required=True,
        to_field_name='metal_id',  # Set the custom column as the value to use
    )
    
    grade = forms.ModelChoiceField(queryset=Grades.objects.filter(is_active=True).order_by('grade_name'),
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'metalChange()'}), label='Grade', required=True)
    
    product_family = forms.ModelChoiceField(queryset=ProductFamilies.objects.filter(is_active=True).order_by('productfamily_name'),
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'getProducts()'}), label='Product Family', required=True,
        to_field_name='productfamily_id',  # Set the custom column as the value to use
    )

    product = forms.ModelChoiceField(queryset=Products.objects.filter(is_active=True).order_by('product_name'),
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'setOuncesValue()'}), label='Product', required=True)
    
    ounces = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-ounces'}), label='Ounces', initial='0.0000', required=True )
    
    metal_quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Quantity',
                                  initial='0',  # Set the default value here 
                                  required=True)
    
    acquisition_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Acquisition Cost',
                                  initial='0.0000',  # Set the default value here 
                                  required=True)
    
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'datepicker'}), label='Purchase Date',
                                    required=True, initial=timezone.now()  # Set default value to the current date and time // ,help_text='Select the purchase date'
    )

    def clean_metal_quantity(self):
        metal_quantity = self.cleaned_data.get('metal_quantity')
        if metal_quantity <= 0:
            raise forms.ValidationError("Metal quantity must be greater than zero.")
        return metal_quantity

    def clean_acquisition_cost(self):
        acquisition_cost = self.cleaned_data.get('acquisition_cost')
        if acquisition_cost <= 0:
            raise forms.ValidationError("Acquisition cost must be greater than zero.")
        return acquisition_cost

    def clean_purchase_date(self):
        purchase_date = self.cleaned_data.get('purchase_date')
        current_date = timezone.now().date()

        if purchase_date > current_date:
            raise forms.ValidationError("Purchase date cannot be in the future.")
        return purchase_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Products.objects.filter(is_active=True).order_by('product_name')

        # Attach related metal to each product family option
        for obj in self.fields['product'].queryset:
            product_family = obj.product_family
            metal = obj.metal
            obj.label = f'{obj.product_name} ({product_family.productfamily_name}) ({metal.metal_name})'
            obj.metal_id = metal.metal_id  # Set a custom attribute for the metal ID
            obj.productfamily_id = product_family.productfamily_id  # Set a custom attribute for the metal ID

    class Meta:
        model = Portfolios
        fields = ['metal','product_family','grade','product','ounces','acquisition_cost','purchase_date']



class EditPortfolioForm(forms.ModelForm):   
    # Add the hidden input field for id
    id = forms.CharField(widget=forms.HiddenInput())
    # metal = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Metal', 'class': 'form-control' 'form-control-ounces'}), label='Metal')
    # grade = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Grade', 'class': 'form-control' 'form-control-ounces'}), label='Grade')
    # product_family = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Product Family', 'class': 'form-control' 'form-control-ounces'}), label='Product Family')
    # product = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Product', 'class': 'form-control' 'form-control-ounces'}), label='Product')
    # ounces = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control' 'form-control-ounces'}), label='Ounces', initial='0.0000', required=True )

    metal_quantity = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Quantity',
                                  initial='0.0000',  # Set the default value here 
                                  required=True)
    
    acquisition_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}), label='Acquisition Cost',
                                  initial='0.0000',  # Set the default value here 
                                  required=True)
    
    purchase_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'id':'datepicker'}), label='Purchase Date',
                                    required=True, initial=timezone.now()  # Set default value to the current date and time // ,help_text='Select the purchase date'
                                    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['product'].queryset = Products.objects.filter(is_active=True).order_by('product_name')

    #     # Attach related metal to each product family option
    #     for obj in self.fields['product'].queryset:
    #         product_family = obj.product_family
    #         metal = obj.metal
    #         obj.label = f'{obj.product_name} ({product_family.productfamily_name}) ({metal.metal_name})'

    class Meta:
        model = Portfolios
        # fields = ['id','metal','product_family','grade','product','ounces','metal_quantity','acquisition_cost','purchase_date']
        fields = ['id','metal_quantity','acquisition_cost','purchase_date']


class DeletePortfolioForm(forms.ModelForm):   
    # Add the hidden input field for id
    id = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = Portfolios
        # fields = ['id','metal','product_family','grade','product','ounces','metal_quantity','acquisition_cost','purchase_date']
        fields = ['id']


class ProductUpdateForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Products
        fields = ['id','is_active', 'factor_rate', 'product_status', 'shipping_status']
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'factor_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_status': forms.Select(attrs={'class': 'form-control'}),
            'shipping_status': forms.Select(attrs={'class': 'form-control'}),
        } 