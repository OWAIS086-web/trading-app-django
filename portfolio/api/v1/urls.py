from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, viewsets

router = DefaultRouter()
app_name = 'portfolio'
router.register(r'active-metals', viewsets.MetalsViewSet, basename='active_metals')
router.register(r'active-grades', viewsets.GradesViewSet, basename='active_grades')
router.register(r'active-asset-classes', viewsets.AssetClassesViewSet, basename='active_asset_classes')
router.register(r'active-products', viewsets.ProductViewSet, basename='active_products')
router.register(r'product-prices-sku', viewsets.ProductPriceViewSet, basename='product_prices_by_sku')

urlpatterns = [
    path("", include(router.urls)),
    # path('grades/', views.GradesView.as_view(), name='grades'),
    path('product-families/', views.ProductFamilyByMetalView.as_view(), name='product_family_by_metal'),
    path('add-portfolio/', views.AddPortfolioAPIView.as_view(), name='add_portfolio'),
    path('update-portfolio/', views.UpdatePortfolioAPIView.as_view(), name='update_portfolio'),
    path('delete-portfolio/', views.DeletePortfolioAPIView.as_view(), name='delete_portfolio'),
    path('user-portfolio-summary/', views.MetalSummarizedDataAPIView.as_view(), name='user_portfolio_summary'),
    path('user-portfolio-by-metal/', views.GetUserPortfolioByMetalAPIView.as_view(), name='user_portfolio_by_metal'),
]