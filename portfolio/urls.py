from django.urls import path
from . import views

app_name = "portfolio"
urlpatterns = [
    # path("", views.portfolio, name="portfolio"),
    path("", views.user_portfolio, name="portfolio"),
    # path("edit-metals/", views.portfolio_update, name="edit_metals"),
    path("list-metals/", views.user_portfolio_list, name="list_metals"),
    path('add/', views.create_portfolio, name='add_portfolio'),
    path('update/<int:id>/', views.update_portfolio, name='update_portfolio_id'),
    path('update/', views.update_portfolio, name='update_portfolio'),
    # path('delete-portfolio/<int:id>', views.delete_portfolio, name='delete_portfolio_id'),
    path('delete/<int:id>/', views.delete_portfolio, name='delete_portfolio_id'),
    path('delete/', views.delete_portfolio, name='delete_portfolio'),
    # path('update/', views.update_portfolio, name='update_portfolio'),
    path('product-families-by-metal/', views.get_product_families_by_metal, name='get_product_families_by_metal'),
    path('products-by-metal-family-grade/', views.get_products_by_metal_family_grade, name='get_products_by_metal_family_grade'),
    path('product-price-by-id/', views.get_products_price_by_id, name='get_products_price_by_id'),

    path("products-list/", views.products_list, name="products_list"),
    path('product/update/<int:product_id>/', views.update_product, name='update_product_id'),
    path('product/update/', views.update_product, name='update_product'),
    

]