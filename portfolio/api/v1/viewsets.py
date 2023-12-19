from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from portfolio.models import *
from .serializers import *

class MetalsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Metals.objects.filter(is_active=True).order_by('metal_name')
    serializer_class = MetalsSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

class GradesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Grades.objects.filter(is_active=True).order_by('grade_name')
    serializer_class = GradesSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions


class AssetClassesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AssetClasses.objects.filter(is_active=True).order_by('assetclass_name')
    serializer_class = AssetClassesSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def get_queryset(self):
        metal_id = self.request.query_params.get('metal_id')
        product_family_id = self.request.query_params.get('product_family_id')
        grade_id = self.request.query_params.get('grade_id')

        queryset = Products.objects.filter(
            metal_id=metal_id,
            product_family_id=product_family_id,
            grade_id=grade_id,
            is_active=True
        ).order_by('product_name')
        return queryset    
    
class ProductPriceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductPriceSerializer
    permission_classes = [IsAuthenticated]  # Add appropriate permissions

    def get_queryset(self):        
        # metal_id = self.request.query_params.get('metal_id')        
        # grade_id = self.request.query_params.get('grade_id')
        product_id = self.request.query_params.get('product_id')

        # Retrieve Product
        product = Products.objects.filter(id=product_id).first()

        sku=product.sku
        metal_name=product.metal.metal_name
        grade_name=product.grade.grade_name

        # sku = self.request.query_params.get('sku')
        # grade = self.request.query_params.get('grade')
        # metal_name = self.request.query_params.get('metal_name')

        # queryset = ProductPrices.objects.filter(sku=product.sku, grade=grade.grade_name, metal_name = metal.metal_name, is_active=True).order_by('-updated').first()        
        # queryset = ProductPrices.objects.filter(is_active=True).order_by('-updated').first()
        
        # queryset = ProductPrices.objects.filter(metal_name = metal_name,grade=grade_name,sku=sku, is_active=True).latest('updated')
        queryset = ProductPrices.objects.filter(
            metal_name=metal_name,
            grade=grade_name,
            sku=sku,
            is_active=True
        ).latest('updated')
        # .first()

        # if queryset.exists():
        #     # Add the factor_rate from the related Product
        #     for item in queryset:
        #         item.factor_rate = product.factor_rate
        
        return [queryset]  # Return as a list to match the expected queryset format
    