from django.contrib import admin
from .models import *
# Register your models here.

    
@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = [ 'grade_name', 'is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]
    autocomplete_fields = ['created_by', 'updated_by']
    list_select_related = ['created_by', 'updated_by']
    readonly_fields = ['grade_name']
    list_filter = ['is_active']
    search_fields = ['grade_name']  # Add the fields you want to search for

    @admin.display(description="Id", ordering="id")
    def display_grade_id_column(self, instance):
        if instance.id:
            return "%s" % instance.id
        return "%s" % instance.id
    
    @admin.display(description="Name", ordering="grade_name")
    def display_grade_name_column(self, instance):
        if instance.grade_name:
            return "%s" % instance.grade_name
        return "%s" % instance.grade_name
    
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
              
    def get_object_by_id(self, object_id):
        try:
            metal = Grades.objects.get(id=object_id)
        except Grades.DoesNotExist:
            metal = None
        return metal

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Metals)
class MetalsAdmin(admin.ModelAdmin):
    list_display = ['metal_id', 'metal_name', 'is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]
    autocomplete_fields = ['created_by', 'updated_by']
    list_select_related = ['created_by', 'updated_by']
    readonly_fields = ['metal_id', 'metal_name']
    list_filter = ['is_active']
    search_fields = ['metal_name']  # Add the fields you want to search for

    @admin.display(description="Id", ordering="metal_id")
    def display_metal_id_column(self, instance):
        if instance.metal_id:
            return "%s" % instance.metal_id
        return "%s" % instance.metal_id
    
    @admin.display(description="Name", ordering="metal_name")
    def display_metal_name_column(self, instance):
        if instance.metal_name:
            return "%s" % instance.metal_name
        return "%s" % instance.metal_name
    
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
              
    def get_object_by_id(self, object_id):
        try:
            metal = Metals.objects.get(id=object_id)
        except Metals.DoesNotExist:
            metal = None
        return metal

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)




@admin.register(AssetClasses)
class AssetClassesAdmin(admin.ModelAdmin):
    list_display = ['assetclass_id', 'assetclass_name','percent_markup', 'is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]
    autocomplete_fields = ['created_by', 'updated_by']
    list_select_related = ['created_by', 'updated_by']
    readonly_fields = ['assetclass_id', 'assetclass_name', 'percent_markup']
    list_filter = ['is_active']
    search_fields = ['assetclass_name']  # Add the fields you want to search for

    @admin.display(description="Id", ordering="assetclass_id")
    def display_assetclass_id_column(self, instance):
        if instance.assetclass_id:
            return "%s" % instance.assetclass_id
        return "%s" % instance.assetclass_id
    
    @admin.display(description="Name", ordering="assetclass_name")
    def display_assetclass_name_column(self, instance):
        if instance.assetclass_name:
            return "%s" % instance.assetclass_name
        return "%s" % instance.assetclass_name
    
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
              
    def get_object_by_id(self, object_id):
        try:
            AssetClass = AssetClasses.objects.get(id=object_id)
        except AssetClass.DoesNotExist:
            AssetClass = None
        return AssetClass

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductFamilies)
class ProductFamiliesAdmin(admin.ModelAdmin):
    list_display = ['productfamily_id', 'productfamily_name','assetclass','parent_id', 'is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]
    autocomplete_fields = ['assetclass','created_by', 'updated_by']
    list_select_related = ['assetclass','created_by', 'updated_by']
    readonly_fields = ['productfamily_id', 'productfamily_name','parent_id']
    list_filter = ['is_active','assetclass']
    search_fields = ['productfamily_name']  # Add the fields you want to search for

    @admin.display(description="Id", ordering="productfamily_id")
    def display_product_family_id_column(self, instance):
        if instance.productfamily_id:
            return "%s" % instance.productfamily_id
        return "%s" % instance.productfamily_id
    
    @admin.display(description="Name", ordering="productfamily_name")
    def display_product_family_name_column(self, instance):
        if instance.productfamily_name:
            return "%s" % instance.productfamily_name
        return "%s" % instance.productfamily_name
    
    @admin.display(description="Asset Class")
    def get_metal(self, instance):
        # Retrieve the asset classes by their IDs
        asset_classes = AssetClasses.objects.filter(assetclass_id__in=instance.assetclass)
        for asset_class in asset_classes:
            return asset_class.assetclass_name
            
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
              
    def get_object_by_id(self, object_id):
        try:
            productfamily = ProductFamilies.objects.get(id=object_id)
        except ProductFamilies.DoesNotExist:
            productfamily = None
        return productfamily

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ['sku','product_name',
                    # 'product_description','product_notes',
                    'metal','grade',
                    # 'product_family','commission','url','thumbnail_url','image_url',
                    # 'base_currency','base_ask','base_bid','cost_source','bid_source','cogs_percent','cogs_dollar','grading_fee','fixed_markup_ask','percent_markup_ask',
                    # 'fixed_markup_bid','percent_markup_bid','fixed_markup_ask_wholesale','percent_markup_ask_wholesale','fixed_markup_bid_wholesale','percent_markup_bid_wholesale',
                    # 'wholesale_notes','track_inventory','retail_shipping','retail_shipping_notes','wholesale_shipping','wholesale_shipping_notes', 
                    'ounces','factor_rate','product_status','shipping_status',
                    'is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]

    autocomplete_fields = ['metal','product_family','grade','created_by', 'updated_by']
    list_select_related = ['metal','product_family','grade','created_by', 'updated_by']
    readonly_fields = ['sku','product_name','metal','grade','ounces',
                       'product_description','product_notes','product_family','commission','url','thumbnail_url','image_url',
                    'base_currency','base_ask','base_bid','cost_source','bid_source','cogs_percent','cogs_dollar','grading_fee','fixed_markup_ask','percent_markup_ask',
                    'fixed_markup_bid','percent_markup_bid','fixed_markup_ask_wholesale','percent_markup_ask_wholesale','fixed_markup_bid_wholesale','percent_markup_bid_wholesale',
                    'wholesale_notes','track_inventory','retail_shipping','retail_shipping_notes','wholesale_shipping','wholesale_shipping_notes',
                    ]
    list_filter = ['metal','grade','product_family','product_status','shipping_status','is_active']
    search_fields = ['product_name']  # Add the fields you want to search for

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'metal':
            kwargs['queryset'] = Metals.objects.filter(is_active=True)

        if db_field.name == 'grade':
            kwargs['queryset'] = Grades.objects.filter(is_active=True)

        if db_field.name == 'product_family':
            kwargs['queryset'] = ProductFamilies.objects.filter(is_active=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    

    @admin.display(description="Sku", ordering="sku")
    def display_product_sku_column(self, instance):
        if instance.sku:
            return "%s" % instance.sku
        return "%s" % instance.sku
    
    @admin.display(description="Name", ordering="product_name")
    def display_product_name_column(self, instance):
        if instance.product_name:
            return "%s" % instance.product_name
        return "%s" % instance.product_name

    @admin.display(description="Metal")
    def get_metal(self, instance):
        # Retrieve the metals by their IDs
        metals = Metals.objects.filter(metal_id__in=instance.metal)
        for metal in metals:
            return metal.metal_name

    @admin.display(description="Product Family")
    def get_product_family(self, instance):
        # Retrieve the families by their IDs
        families = ProductFamilies.objects.filter(productfamily_id__in=instance.product_family)
        for family in families:
            return family.productfamily_name
        
    @admin.display(description="Grade")
    def get_product_grade(self, instance):
        # Retrieve the grade by their IDs
        grades = Grades.objects.filter(grade_id__in=instance.grade)
        for grade in grades:
            return grade.grade_name
                
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
              
    def get_object_by_id(self, object_id):
        try:
            product = Products.objects.get(id=object_id)
        except Products.DoesNotExist:
            product = None
        return product

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductPrices)
class ProductPricesAdmin(admin.ModelAdmin):
    list_display = ['sku','product_name','metal_name','productfamily_name','assetclass_name','grade','ounces','cogs','bid','ask','base_ask','cost_source',
                    'base_currency','description','retail_shipping','wholesale_shipping','is_active', 'created', 
                    # 'created_by', 'updated', 'updated_by'
                    ]
    
    autocomplete_fields = ['created_by', 'updated_by']
    list_select_related = ['created_by', 'updated_by']

    readonly_fields = ['sku','product_name','metal_name','productfamily_name','assetclass_name','grade','ounces','cogs','bid','ask','base_ask','cost_source',
                       'base_currency','description','retail_shipping','wholesale_shipping',]

    list_filter = ['metal_name','productfamily_name','assetclass_name','grade','is_active']
    
    search_fields = ['sku','productfamily_name','product_name']  # Add the fields you want to search for

    @admin.display(description="Sku", ordering="sku")
    def display_product_sku_column(self, instance):
        if instance.sku:
            return "%s" % instance.sku
        return "%s" % instance.sku
    
    @admin.display(description="Name", ordering="product_name")
    def display_product_name_column(self, instance):
        if instance.product_name:
            return "%s" % instance.product_name
        return "%s" % instance.product_name
       
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
              
    def get_object_by_id(self, object_id):
        try:
            price = ProductPrices.objects.get(id=object_id)
        except ProductPrices.DoesNotExist:
            price = None
        return price

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Portfolios)
class PortfoliosAdmin(admin.ModelAdmin):
    list_display = ['metal','product_family','grade','sku','product','ounces','metal_quantity','acquisition_cost',
                    # 'metal_value',
                    'purchase_date',
                    'is_deleted', 'created', 'created_by', 'updated', 'updated_by']
    autocomplete_fields = ['metal','product_family','grade','product','created_by', 'updated_by']
    list_select_related = ['metal','product_family','grade','product','created_by', 'updated_by']
    readonly_fields = ['metal','product_family','grade','sku','product','ounces','metal_quantity','acquisition_cost','metal_value'] 
    list_filter = ['metal','product_family','grade','is_deleted']
    search_fields = ['product']  # Add the fields you want to search for

    @admin.display(description="Id", ordering="id")
    def display_portfolio_id_column(self, instance):
        if instance.id:
            return "%s" % instance.id
        return "%s" % instance.id
    
    @admin.display(description="Metal")
    def get_metal(self, instance):
        # Retrieve the metals by their IDs
        metals = Metals.objects.filter(metal_id__in=instance.metal)
        for metal in metals:
            return metal.metal_name

    @admin.display(description="Product Family")
    def get_portfolio_product_family(self, instance):
        # Retrieve the families by their IDs
        families = ProductFamilies.objects.filter(productfamily_id__in=instance.product_family)
        for family in families:
            return family.productfamily_name
        
    @admin.display(description="Product")
    def get_portfolio_product(self, instance):
        # Retrieve the products by their IDs
        products = Products.objects.filter(product_id__in=instance.product)
        for product in products:
            return product.product_name
                
    @admin.display(description="Grade")
    def get_portfolio_grade(self, instance):
        # Retrieve the products by their IDs
        grades = Grades.objects.filter(grade_id__in=instance.product)
        for grade in grades:
            return grade.grade_name
                        
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
              
    def get_object_by_id(self, object_id):
        try:
            portfolio = Portfolios.objects.get(id=object_id)
        except Portfolios.DoesNotExist:
            portfolio = None
        return portfolio

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)