import os
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from modules.model_mixins import TimeStampModel
from users.models import *
# Create your models here.

class Metals(TimeStampModel):    
    metal_id = models.CharField(_("Id"), blank=False, null=False, editable=False, unique=True, default='', max_length=125)
    metal_name = models.CharField(_("Name"), blank=False, null=False, default='metal', max_length=150)
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_metal', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_metal', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return self.metal_name
    
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Metal')
        verbose_name_plural = _('Priority Gold Metals')

class Grades(TimeStampModel):    
    grade_name = models.CharField(_("Name"), blank=False, null=False, default='grade', max_length=150)
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_grade', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_grade', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return self.grade_name
    
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Metal Grade')
        verbose_name_plural = _('Priority Gold Metal Grades')


class AssetClasses(TimeStampModel):    
    assetclass_id = models.CharField(_("Id"), blank=False, null=False, editable=False, unique=True, default='', max_length=125)
    assetclass_name = models.CharField(_("Name"), blank=False, null=False, default='asset class', max_length=150)
    percent_markup = models.DecimalField(_("Percent Markup"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_assetclass', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_assetclass', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return self.assetclass_name
    
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Asset Class')
        verbose_name_plural = _('Priority Gold Asset Classes')

class ProductFamilies(TimeStampModel):    
    productfamily_id = models.CharField(_("Id"), blank=False, null=False, editable=False,unique=True, default='', max_length=125)
    productfamily_name = models.CharField(_("Name"), blank=False, null=False, default='product family', max_length=250)
    # assetclass_id = models.CharField(_("Asset Class Id"), null=True, blank=True, editable=False, default='', max_length=125)
    assetclass = models.ForeignKey(AssetClasses, on_delete=models.SET_NULL,to_field='assetclass_id', null=True, blank=True, editable=False, related_name='productfamily_assetclass', verbose_name=_("Asset Class"))
    parent_id = models.CharField(_("Parent Id"), null=True, blank=True, editable=False, default='', max_length=125)
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_product_family', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_product_family', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    def __str__(self):
        return self.productfamily_name
    
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Product Family')
        verbose_name_plural = _('Priority Gold Product Families')

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


class Products(TimeStampModel):    
    sku = models.CharField(_("SKU"), blank=False, null=False, editable=False, default='-', max_length=20)    
    product_name = models.CharField(_("Name"), blank=False, null=False, default='product name', max_length=250)
    product_description = models.CharField(_("Description"), null=True, default='description', max_length=500)
    product_notes = models.CharField(_("Notes"), null=True, default='note', max_length=500)
    metal = models.ForeignKey(Metals, on_delete=models.SET_NULL,to_field='metal_id', null=True, blank=True, editable=False, related_name='product_metal', verbose_name=_("Metal"))
    ounces = models.DecimalField(_("Ounces"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)       
    product_family = models.ForeignKey(ProductFamilies, on_delete=models.SET_NULL,to_field='productfamily_id', null=True, blank=True, editable=False, related_name='product_productfamily', verbose_name=_("Product Family"))   
    # grade = models.ForeignKey(Grades, on_delete=models.SET_NULL,to_field='grade_name', null=True, blank=True, editable=False, related_name='product_grade', verbose_name=_("Grade"))
    grade = models.ForeignKey(Grades, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='product_grade', verbose_name=_("Grade"))
    # grade = models.CharField(_("Grade"), blank=False, null=False, editable=False, default='-', max_length=25)    
    commission = models.DecimalField(_("Commission"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    url = models.CharField(_("Url"), null=True, blank=True, default='#', max_length=500)
    thumbnail_url = models.CharField(_("Thumbnail Url"), null=True, blank=True, default='#', max_length=500)
    image_url = models.CharField(_("Image Url"), null=True, blank=True, default='#', max_length=500)
    base_currency = models.CharField(_("Base Currency"), null=True, blank=True, default='USD', max_length=15)
    base_ask = models.DecimalField(_("Base Ask"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    base_bid = models.DecimalField(_("Base Bid"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    cost_source = models.CharField(_("Cost Source"), null=True, blank=True, default='-', max_length=20)
    bid_source = models.CharField(_("Bid Source"), null=True, blank=True, default='-', max_length=20)
    cogs_percent = models.DecimalField(_("Cogs Percent"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    cogs_dollar = models.DecimalField(_("Cogs Dollar"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    grading_fee = models.DecimalField(_("Grading Fee"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    fixed_markup_ask = models.DecimalField(_("Fixed Markup Ask"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    percent_markup_ask = models.DecimalField(_("Percent Markup Ask"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    fixed_markup_bid = models.DecimalField(_("Fixed Markup Bid"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    percent_markup_bid = models.DecimalField(_("Percent Markup Bid"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    fixed_markup_ask_wholesale = models.DecimalField(_("Fixed Markup Ask Wholesale"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    percent_markup_ask_wholesale = models.DecimalField(_("Percent Markup Ask Wholesale"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    fixed_markup_bid_wholesale = models.DecimalField(_("Fixed Markup Bid Wholesale"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    percent_markup_bid_wholesale = models.DecimalField(_("Percent Markup Bid Wholesale"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    wholesale_notes = models.CharField(_("Wholesale Notes"), null=True, default='note', max_length=500)
    track_inventory = models.BooleanField(_("Track Inventory"), null=True)
    retail_shipping = models.DecimalField(_("Retail Shipping"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    retail_shipping_notes = models.CharField(_("Retail Shipping Notes"), null=True, default='note', max_length=500)
    wholesale_shipping = models.DecimalField(_("Wholesale Shipping"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    wholesale_shipping_notes = models.CharField(_("Wholesale Shipping Notes"), null=True, default='note', max_length=500)

    factor_rate = models.DecimalField(_("Factor Rate"), max_digits=8,decimal_places=4, default=0.0000, blank=False, null=False, editable=True)
    product_status = models.PositiveIntegerField(choices=PRODUCT_STATUS_CHOICES, null=True)
    shipping_status = models.PositiveIntegerField(choices=SHIPPING_STATUS_CHOICES, null=True)
    
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_product', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_product', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    # def __str__(self):
    #     return self.product_name

    def __str__(self):
        metal_name = self.metal.metal_name if self.metal else "No Metal"
        product_family_name = self.product_family.productfamily_name if self.product_family else "No Product Family"
        grade_name = self.grade.grade_name if self.grade else "No Grade"
        product_name = self.product_name if self.product_name else "No Product"
        
        return f"{metal_name} - {grade_name} - {product_family_name} - {product_name}"
        
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Product')
        verbose_name_plural = _('Priority Gold Products')

class ProductPrices(TimeStampModel):    
    sku = models.CharField(_("SKU"), blank=False, null=False, editable=False, default='-', max_length=20)    
    product_name = models.CharField(_("Name"), blank=False, null=False, default='product name', max_length=250)
    metal_name = models.CharField(_("Metal"), blank=False, null=False, default='metal', max_length=150)
    productfamily_name = models.CharField(_("Product Family"), blank=False, null=False, default='product family', max_length=250)
    assetclass_name = models.CharField(_("Asset Class"), blank=False, null=False, default='asset class', max_length=150)
    grade = models.CharField(_("Grade"), blank=False, null=False, editable=False, default='-', max_length=25)    

    ounces = models.DecimalField(_("Ounces"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)       
    cogs = models.DecimalField(_("Cogs"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    bid = models.DecimalField(_("Bid"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    ask = models.DecimalField(_("Ask"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    base_ask = models.DecimalField(_("Base Ask"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    cost_source = models.CharField(_("Cost Source"), null=True, blank=True, default='-', max_length=20)
    base_currency = models.CharField(_("Base Currency"), null=True, blank=True, default='USD', max_length=15)
    description = models.CharField(_("Description"), null=True, default='description', max_length=500)
    retail_shipping = models.DecimalField(_("Retail Shipping"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)    
    wholesale_shipping = models.DecimalField(_("Wholesale Shipping"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=False)
        
    is_active = models.BooleanField(_("Is Active?"), null=False,default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_user_productprice', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_user_productprice', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    # def __str__(self):
    #     return self.product_name

    def __str__(self):
        metal_name = self.metal_name if self.metal_name else "No Metal"
        product_family_name = self.productfamily_name if self.productfamily_name else "No Product Family"
        grade_name = self.grade if self.grade else "No Grade"
        product_sku = self.sku if self.sku else "No Sku"
        product_name = self.product_name if self.product_name else "No Product"
        product_ounces = self.ounces if self.ounces else "No Ounces"
        
        return f"{metal_name} - {grade_name} - {product_family_name} - {product_sku} - {product_name} - {product_ounces}"
        
    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('Priority Gold Product Price')
        verbose_name_plural = _('Priority Gold Product Prices')


# GRADE_BU = 'BU'
# GRADE_BULLION = 'Bullion'
# GRADE_CIRC = 'Circ'
# GRADE_PRE_1933_US_GOLD_COINS = 'pre-1933 US Gold Coins'
# GRADE_PROOF = 'Proof'

# GRADE_CHOICES = (
#     (GRADE_BU, _('BU')),
#     (GRADE_BULLION, _('Bullion')),
#     (GRADE_CIRC, _('Circ')),
#     (GRADE_PRE_1933_US_GOLD_COINS, _('pre-1933 US Gold Coins')),
#     (GRADE_PROOF, _('Proof')),
#     )

class Portfolios(TimeStampModel):
    metal = models.ForeignKey(Metals, on_delete=models.SET_NULL,to_field='metal_id', null=True, blank=True, editable=True, related_name='portfolio_metal', verbose_name=_("Metal"))
    product_family = models.ForeignKey(ProductFamilies, on_delete=models.SET_NULL,to_field='productfamily_id', null=True, blank=True, editable=True, related_name='portfolio_productfamily', verbose_name=_("Product Family"))
    # grade = models.CharField(_("Grade"), choices=GRADE_CHOICES, max_length=25, editable=True, null=False, blank=False)
    grade = models.ForeignKey(Grades, on_delete=models.SET_NULL, null=True, blank=True, editable=True, related_name='portfolio_product_grade', verbose_name=_("Grade"))
    sku = models.CharField(_("SKU"), null=False, blank=False, editable=True, default='-', max_length=20)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True, blank=True, editable=True, related_name='portfolio_product', verbose_name=_("Product"))
    ounces = models.DecimalField(_("Ounces"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=True)
    # metal_quantity = models.DecimalField(_("Quantity"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=True)
    metal_quantity = models.IntegerField(_("Quantity"), default=0, blank=False, null=False, editable=True)
    acquisition_cost = models.DecimalField(_("Acquisition Cost"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=True)
    metal_value = models.DecimalField(_("Metal Value"), max_digits=10,decimal_places=4, default=0.0000, blank=False, null=False, editable=True)
    purchase_date = models.DateField(_("Purchase Date"), default=timezone.now, blank=False, null=False, editable=True)
    is_deleted = models.BooleanField(_("Is Deleted?"), null=False,default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='created_by_portfolio', verbose_name=_("Created By"))
    # created_on = models.DateTimeField(_("Created On"), auto_now_add=True, blank=False, null=False, editable=False)    
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, editable=False, related_name='updated_by_portfolio', verbose_name=_("Updated By"))
    # updated_on = models.DateTimeField(_("Updated On"), auto_now_add=True, blank=False, null=False, editable=False)

    # def __str__(self):
    #     return self.product.product_name
    
    def __str__(self):
        metal_name = self.metal.metal_name if self.metal else "No Metal"
        product_family_name = self.product_family.productfamily_name if self.product_family else "No Product Family"
        grade_name = self.grade.grade_name if self.grade else "No Grade"
        product_sku = self.sku if self.product else "No Sku"
        product_name = self.product.product_name if self.product else "No Product"
        
        return f"{metal_name} - {grade_name} - {product_family_name} - {product_sku} - {product_name}"


    class Meta:
        # ordering = ('-updated_on',)
        ordering = ('-updated',)
        verbose_name = _('User Metal Portfolio')
        verbose_name_plural = _('User Metal Portfolios')