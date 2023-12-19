from rest_framework import serializers
from portfolio.models import *


class MetalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metals
        fields = '__all__'

class AssetClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetClasses
        fields = '__all__'

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = '__all__'

class ProductFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFamilies
        fields = '__all__'    

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'        

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrices
        fields = '__all__'        

# class PortfolioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Portfolios
#         fields = '__all__'        

class PortfolioSerializer(serializers.ModelSerializer):
    metal_name = serializers.CharField(source='metal.metal_name', read_only=True)
    grade_name = serializers.CharField(source='grade.grade_name', read_only=True)
    product_family_name = serializers.CharField(source='product_family.productfamily_name', read_only=True)
    product_name = serializers.CharField(source='product.product_name', read_only=True)

    class Meta:
        model = Portfolios
        fields = ['id','created','updated','sku','ounces','metal_quantity','acquisition_cost','metal_value','purchase_date',
                  'is_deleted','metal','metal_name','grade','grade_name','product_family','product_family_name','product',
                  'product_name','created_by','updated_by']
        
class SummarizedMetalSerializer(serializers.Serializer):
    metal_id = serializers.CharField()
    metal_name = serializers.CharField()
    total_ounces = serializers.DecimalField(max_digits=10, decimal_places=4)
    # total_metal_quantity = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_metal_quantity = serializers.IntegerField()
    # total_acquisition_value = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_acquisition_value = serializers.IntegerField()
    # total_current_value = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_current_value = serializers.IntegerField()
    # total_difference_value = serializers.DecimalField(max_digits=10, decimal_places=4)
    total_difference_value = serializers.IntegerField()
    total_percentage_change = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        # model = Portfolios
        fields = ['metal_name','metal_quantity','acquisition_value','current_value','difference_value'
                #   ,'percentage_change'
                ]    