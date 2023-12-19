from django.urls import reverse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from django.contrib import messages
from .forms import PortfolioForm,EditPortfolioForm,DeletePortfolioForm,ProductUpdateForm
from .models import *
from django.http import JsonResponse
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Sum, F, Subquery, OuterRef, Min, Max
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from collections import defaultdict
import json
from decimal import Decimal


def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    raise TypeError("Object of type '{}' is not JSON serializable".format(type(obj)))


@login_required
# @csrf_protect  # Apply CSRF protection
def get_product_families_by_metal(request):
    print("User is authenticated:", request.user.is_authenticated)
    metal_id = request.GET.get('metal_id')
    grade_id = request.GET.get('grade_id')
    products = Products.objects.filter(metal_id=metal_id, grade_id=grade_id, is_active=True)
    # Extract product family IDs from the products queryset
    productfamily_ids = products.values_list('product_family_id', flat=True)
    # Filter ProductFamilies based on the extracted product family IDs
    product_families = ProductFamilies.objects.filter(productfamily_id__in=productfamily_ids, is_active=True).order_by('productfamily_name')
    # Convert the product_families queryset into a list of dictionaries
    product_families_serialized = serializers.serialize('json', product_families)
    return JsonResponse({'product_families': product_families_serialized}, safe=False)

@login_required
def get_products_by_metal_family_grade(request):
    print("User is authenticated:", request.user.is_authenticated)
    metal_id = request.GET.get('metal_id')
    grade_id = request.GET.get('grade_id')
    product_family_id = request.GET.get('product_family_id')
    products = Products.objects.filter(metal_id=metal_id, grade_id=grade_id, product_family_id=product_family_id, is_active=True).order_by('product_name')
    products_serialized = serializers.serialize('json', products)
    return JsonResponse({'products': products_serialized}, safe=False)

@login_required
def get_products_price_by_id(request):
    # print("User is authenticated:", request.user.is_authenticated)
    product_id = request.GET.get('product_id')    
    product = Products.objects.filter(id=product_id).first()

    if product:
        sku = product.sku
        factor_rate = product.factor_rate
        metal_name =  product.metal.metal_name
        grade_name = product.grade.grade_name            
        # print(sku)            
        product_price = ProductPrices.objects.filter(
                metal_name=metal_name,
                grade=grade_name,
                sku=sku,
                is_active=True
            ).latest('updated')      

        product_data = {
                    'sku': sku,
                    'factor_rate':factor_rate,
                    'metal_name': metal_name,
                    'grade_name': grade_name,
                    'cogs': product_price.cogs,
                    'bid': product_price.bid,
                    'ask': product_price.ask,
                    'base_ask': product_price.base_ask,
                }
        
        # products_serialized = serializers.serialize('json', product_price)
        # return JsonResponse(product_price)
        return JsonResponse(product_data)
    else:
        return JsonResponse({'error': 'Product not found'}, status=404)


@login_required
def create_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data.get('product')
            if prod:
                instance = form.save(commit=False)
                instance.sku = prod.sku 
                instance.metal_quantity = form.cleaned_data.get('metal_quantity', 0.0)
                instance.metal_value = form.cleaned_data.get('acquisition_cost', 0.0)
                instance.created_by = request.user
                instance.updated_by = request.user
                instance.save()
                messages.success(request, 'Portfolio created successfully.')
                context = {"head_title": "Portfolio | Priority Gold Plus"}
                return redirect('portfolio:portfolio')  # Redirect to the portfolio list page or wherever appropriate
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
            form = PortfolioForm(request.POST)            
            context = {'form': form, "head_title": "Add Metals | Priority Gold Plus"}
            return render(request, 'add_portfolio.html', context)            
    else:
        form = PortfolioForm()
        context = {'form': form, "head_title": "Add Metals | Priority Gold Plus"}
        return render(request, 'add_portfolio.html', context)

def get_metal_color(metal_name):
    if metal_name == 'Gold':
        return '#D9A518'
    elif metal_name == 'Silver':
        return '#B9B9B9'
    elif metal_name == 'Palladium':
        return '#8E8E8E'
    elif metal_name == 'Platinum':
        return '#9B9B6E'     
    else:
        return '#000000'  # Default color if metal_name doesn't match any condition



@login_required
def user_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data.get('product')
            if prod:
                instance = form.save(commit=False)
                instance.sku = prod.sku 
                instance.metal_quantity = form.cleaned_data.get('metal_quantity', 0.0)
                instance.metal_value = form.cleaned_data.get('acquisition_cost', 0.0)
                instance.created_by = request.user
                instance.updated_by = request.user
                instance.save()
                messages.success(request, 'Portfolio created successfully.')
                return redirect('portfolio')  # Redirect to the portfolio list page or wherever appropriate
            else:
                messages.error(request, 'Invalid product selected.')
                form = PortfolioForm(request.POST)
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
            form = PortfolioForm(request.POST)
            context = {'form': form, "head_title": "Edit Metals | Priority Gold Plus"}
            return render(request, 'new_portfolio.html', context)
    else:
        # Get the logged-in user
        user = request.user
        # Retrieve the user's portfolios
        user_portfolios = Portfolios.objects.filter(created_by=user, is_deleted=False)
        if user_portfolios.exists():
            distinct_metals = []
            portfolio_data = []

            for portfolio in user_portfolios:
                # Check if the metal is not already in the distinct_metals list
                if portfolio.metal not in distinct_metals:
                    # Add the metal to the distinct_metals list
                    distinct_metals.append(portfolio.metal)

            for portfolio in user_portfolios:

                product = portfolio.product        
                product_family = portfolio.product_family
                metal = portfolio.metal
                grade = portfolio.grade

                # Get the latest product price for the product
                latest_price = ProductPrices.objects.filter(sku=product.sku, metal_name = metal.metal_name, grade = grade.grade_name, is_active=True).latest('updated')

                # Calculate the acquisition value and current value
                acquisition_value =0.0000
                # acquisition_value = round(float(portfolio.metal_value), 0)
                acquisition_value = portfolio.metal_value
                # Convert current_value to an integer
                # acquisition_value = int(acquisition_value)

                current_value = 0.0000  # Default current value
                metal_quantity = 0.0000

                if latest_price:            
                    metal_quantity = portfolio.metal_quantity
                    cogs = latest_price.cogs
                    bid = latest_price.bid
                    ask = latest_price.ask
                    base_ask = latest_price.base_ask
                    cost_source = latest_price.cost_source
                    last_updated = latest_price.updated
                    # current_value = ((latest_price.ask * product.factor_rate) * portfolio.metal_quantity)
                    current_value = ((latest_price.ask * portfolio.metal_quantity) * product.factor_rate)

                # Calculate last_updated in two formats: MM/DD/YYYY and "X mins ago"
                if last_updated:
                    # last_updated_date = last_updated.strftime("%m/%d/%Y")
                    # Format last_updated in the desired format "MM/DD/YYYY HH:MM:SS AM/PM"
                    last_updated_date = last_updated.strftime("%m/%d/%Y %I:%M:%S %p")

                    time_difference = timezone.now() - last_updated
                    mins_difference = time_difference.seconds // 60

                    if mins_difference < 60:
                        last_updated_mins_ago = f"{mins_difference} mins ago"
                    else:
                        last_updated_mins_ago = None

                # Calculate the difference between current_value and acquisition_value
                difference_value = 0.0000
                difference_value = current_value - acquisition_value

                if acquisition_value == 0:
                    percentage_change = 0
                else:
                    percentage_change = ((current_value - acquisition_value) / acquisition_value) * 100

                # Convert current_value to an integer
                acquisition_value = int(acquisition_value)
                # Convert current_value to an integer
                current_value = int(current_value)
                
                # Create a dictionary with portfolio data
                portfolio_entry = {
                    'portfolio': portfolio,
                    'metal': metal,
                    'product_family': product_family,
                    'grade': grade,
                    'product': product,
                    'ounces' : product.ounces,
                    'metal_quantity': metal_quantity,
                    'acquisition_value': acquisition_value,
                    'current_value': current_value,
                    # 'percentage_change': round(percentage_change, 2),
                    'difference_value': difference_value,
                    # 'profit_loss_flag': profit_loss_flag,
                    # 'min_ask': rate_summary.get(metal=metal.metal_name, product=product.product_name,sku=product.sku).get('min_rate'),
                    # 'max_ask': rate_summary.get(metal=metal.metal_name, product=product.product_name,sku=product.sku).get('max_rate'),
                    'last_updated_date': last_updated_date,
                    'last_updated_mins_ago': last_updated_mins_ago,            
                }

                # Add the portfolio data to the list
                portfolio_data.append(portfolio_entry)

                # Create a list to hold the summarized metal-wise data
                summarized_metal_data = []
                summarized_metal_total_data = []
                summarized_metal_graph_data = []

                # Sort portfolio_data list by 'metal_name'
                sorted_portfolio_data = sorted(portfolio_data, key=lambda x: x['metal'].metal_name)


                # Initialize variables to store metal-wise sums
                metal_quantity_sum = 0
                acquisition_value_sum = 0
                current_value_sum = 0
                difference_value_sum = 0
                percentage_change = 0
                
                current_metal = None  # Initialize to None

            # Loop through sorted portfolio_data list and create entries for summarized_metal_data
            for entry in sorted_portfolio_data:
                metal_name = entry['metal'].metal_name

                # Check if the metal has changed
                if current_metal is None or current_metal != metal_name:
                    # Calculate percentage change only if acquisition_value_sum is not 0
                    if acquisition_value_sum == 0:
                        percentage_change_sum = 0
                    else:
                        percentage_change_sum = ((current_value_sum - acquisition_value_sum) / acquisition_value_sum) * 100

                    # Reset the sums for the new metal
                    metal_quantity_sum = 0
                    acquisition_value_sum = 0
                    current_value_sum = 0
                    difference_value_sum = 0

                    current_metal = metal_name

                metal_quantity_sum += (entry['metal_quantity'] * entry['ounces'])
                acquisition_value_sum += entry['acquisition_value']
                current_value_sum += entry['current_value']
                difference_value_sum += entry['difference_value']

                if acquisition_value_sum == 0:
                    percentage_change = 0
                else:
                    percentage_change = ((current_value_sum - acquisition_value_sum) / acquisition_value_sum) * 100

                metal_entry = {
                    'metal_name': metal_name,
                    'metal_quantity': metal_quantity_sum,
                    'acquisition_value': acquisition_value_sum,
                    'current_value': current_value_sum,
                    'difference_value': difference_value_sum,
                    'percentage_change': round(percentage_change, 2),
                }

                metal_graph_entry = {
                    'labels': metal_name,
                    'values': metal_quantity_sum,
                    'colors': get_metal_color(metal_name)
                }

                # Check if the metal entry already exists in summarized_metal_data
                existing_metal_entry = next((item for item in summarized_metal_data if item['metal_name'] == metal_name), None)
                
                if existing_metal_entry:
                    # Update the existing entry
                    existing_metal_entry.update(metal_entry)
                else:
                    # Add the new entry
                    summarized_metal_data.append(metal_entry)


                # Check if the metal entry already exists in summarized_metal_data
                existing_metal_graph_entry = next((item for item in summarized_metal_graph_data if item['labels'] == metal_name), None)
                
                if existing_metal_graph_entry:
                    # Update the existing entry
                    existing_metal_graph_entry.update(metal_graph_entry)
                else:
                    # Add the new entry
                    summarized_metal_graph_data.append(metal_graph_entry)


                total_metal_quantity = sum(entry['metal_quantity'] for entry in summarized_metal_data)
                total_acquisition_value = sum(entry['acquisition_value'] for entry in summarized_metal_data)
                total_current_value = sum(entry['current_value'] for entry in summarized_metal_data)
                total_difference_value = sum(entry['difference_value'] for entry in summarized_metal_data)
                total_percentage_change = ((total_current_value - total_acquisition_value) / total_acquisition_value) * 100

                # Determine if it's a profit or loss based on the percentage change
                if total_current_value > total_acquisition_value:
                    profit_loss_flag = "Profit"
                elif total_current_value < total_acquisition_value:
                    profit_loss_flag = "Loss"
                else:
                    profit_loss_flag = "No Change"

                portfolio_total_entry = {
                'metal_quantity': total_metal_quantity,
                'acquisition_value': total_acquisition_value,
                'current_value': total_current_value,
                'difference_value': total_difference_value,
                'percentage_change': round(total_percentage_change, 2),
                'profit_loss_flag': profit_loss_flag,
                }

            # Convert the portfolio_total_entry dictionary to JSON-formatted string with double quotes
            # portfolio_total_json = json.dumps(portfolio_total_entry, ensure_ascii=False)
            portfolio_total_json = json.dumps(portfolio_total_entry, default=convert_decimal, ensure_ascii=False)
            summarized_metal_graph_data_json = json.dumps(summarized_metal_graph_data, default=convert_decimal, ensure_ascii=False)

            # Render the template with the portfolio data
            # context = {"head_title": "Portfolio | Priority Gold Plus",'portfolio_data': portfolio_data, 'distinct_metals': distinct_metals,'metal_summary': metal_summary,}
            context = {"head_title": "Portfolio | Priority Gold Plus",'portfolio_data': portfolio_data,'distinct_metals': distinct_metals,'summarized_metal_data':summarized_metal_data,'portfolio_total_data':portfolio_total_json,'portfolio_total':portfolio_total_entry, 'summarized_metal_graph_data':summarized_metal_graph_data_json,}
            return render(request, 'portfolio.html', context)    
        else:
            form = PortfolioForm()
            context = {'form': form, "head_title": "Add Metals | Priority Gold Plus"}
            return render(request, 'new_portfolio.html', context)        


@login_required
def user_portfolio_list(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            prod = form.cleaned_data.get('product')
            if prod:
                instance = form.save(commit=False)
                instance.sku = prod.sku 
                instance.metal_quantity = form.cleaned_data.get('metal_quantity', 0.0)
                instance.metal_value = form.cleaned_data.get('acquisition_cost', 0.0)
                instance.created_by = request.user
                instance.updated_by = request.user
                instance.save()
                messages.success(request, 'Portfolio created successfully.')
                return redirect('portfolio')  # Redirect to the portfolio list page or wherever appropriate
            else:
                messages.error(request, 'Invalid product selected.')
                form = PortfolioForm(request.POST)
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
            form = PortfolioForm(request.POST)
            context = {'form': form, "head_title": "Edit Metals | Priority Gold Plus"}
            return render(request, 'new_portfolio.html', context)

    else:            
        # Get the logged-in user
        user = request.user
        # Retrieve the user's portfolios
        user_portfolios = Portfolios.objects.filter(created_by=user, is_deleted=False).order_by('metal')
        if user_portfolios.exists():
            # Create a list to hold the portfolio data with calculated values
            portfolio_data = []
            distinct_metals = []
            # Loop through each portfolio and calculate acquisition value and current value
            for portfolio in user_portfolios:
                # Check if the metal is not already in the distinct_metals list
                if portfolio.metal not in distinct_metals:
                    # Add the metal to the distinct_metals list
                    distinct_metals.append(portfolio.metal)

                product = portfolio.product        
                product_family = portfolio.product_family
                metal = portfolio.metal
                grade = portfolio.grade
                pu_date = portfolio.purchase_date
                portfolio_id = portfolio.id

                if pu_date:
                    purchase_date = pu_date.strftime("%m/%d/%Y")

                # Get the latest product price for the product
                latest_price = ProductPrices.objects.filter(sku=product.sku, metal_name = metal.metal_name, grade = grade.grade_name, is_active=True).latest('updated')
                # Calculate the acquisition value and current value
                acquisition_value =0.0000           
                acquisition_value = portfolio.metal_value
                # Convert current_value to an integer
                # acquisition_value = int(acquisition_value)

                current_value = 0.0000  # Default current value
                metal_quantity = 0.0000

                if latest_price:            
                    metal_quantity = portfolio.metal_quantity
                    cogs = latest_price.cogs
                    bid = latest_price.bid
                    ask = latest_price.ask
                    base_ask = latest_price.base_ask
                    cost_source = latest_price.cost_source
                    last_updated = latest_price.updated
                    # current_value = latest_price.ask * portfolio.metal_quantity
                    current_value = ((latest_price.ask * portfolio.metal_quantity) * product.factor_rate)

                # Calculate last_updated in two formats: MM/DD/YYYY and "X mins ago"
                if last_updated:
                    last_updated_date = last_updated.strftime("%m/%d/%Y %I:%M:%S %p")
                    time_difference = timezone.now() - last_updated
                    mins_difference = time_difference.seconds // 60

                    if mins_difference < 60:
                        last_updated_mins_ago = f"{mins_difference} mins ago"
                    else:
                        last_updated_mins_ago = None

                # Calculate the difference between current_value and acquisition_value
                difference_value = 0.0000
                difference_value = current_value - acquisition_value

                if acquisition_value == 0:
                    percentage_change = 0
                else:
                    percentage_change = ((current_value - acquisition_value) / acquisition_value) * 100
                
                # Determine if it's a profit or loss based on the percentage change
                if current_value > acquisition_value:
                    profit_loss_flag = "Profit"
                elif current_value < acquisition_value:
                    profit_loss_flag = "Loss"
                else:
                    profit_loss_flag = "No Change"        

                # Create a dictionary with portfolio data
                portfolio_entry = {
                    'portfolio': portfolio,
                    'portfolio_id':portfolio_id,
                    'metal': metal,
                    'product_family': product_family,
                    'grade': grade,
                    'product': product,
                    'ounces': product.ounces,
                    'purchase_date':purchase_date,
                    'metal_quantity':metal_quantity,            
                    'acquisition_value': acquisition_value,
                    'cogs': cogs,
                    'bid': bid,
                    'ask': ask,
                    'base_ask': base_ask,
                    'cost_source': cost_source,
                    'current_value': current_value,
                    'percentage_change': round(percentage_change, 2),
                    'difference_value': difference_value,
                    'profit_loss_flag': profit_loss_flag,
                    'last_updated_date': last_updated_date,
                    'last_updated_mins_ago': last_updated_mins_ago,            
                }

                #  Add the portfolio data to the list
                portfolio_data.append(portfolio_entry)
            # # Render the template with the portfolio data
            context = {"head_title": "Edit Portfolio | Priority Gold Plus",'portfolio_data': portfolio_data, 'distinct_metals': distinct_metals,}
            return render(request, 'list_portfolio.html', context)
        else:
            # No portfolio data, render the add_metal.html template
            form = PortfolioForm()
            context = {'form': form, "head_title": "Add Metals | Priority Gold Plus"}
            return render(request, 'new_portfolio.html', context)        


@login_required
def update_portfolio(request, id):
    
    # portfolio = Portfolios.objects.filter(id=id).first()
    portfolio = get_object_or_404(Portfolios, id=id)

    if request.method == 'GET':        
        form = EditPortfolioForm(instance=portfolio)
        context = {
            'form': form,
            'metal_name': portfolio.metal.metal_name,
            'grade_name': portfolio.grade.grade_name,
            'productfamily_name': portfolio.product_family.productfamily_name,
            'product_name': portfolio.product.product_name,
            'metal_quantity': portfolio.metal_quantity,
            'ounces': portfolio.ounces,
            'head_title': "Edit Metals | Priority Gold Plus"
        }
        return render(request, 'update_portfolio.html', context)

    if request.method == 'POST':
        form = EditPortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.metal_quantity = form.cleaned_data.get('metal_quantity', 0.0)
            instance.metal_value = form.cleaned_data.get('acquisition_cost', 0.0)
            instance.purchase_date = form.cleaned_data.get('purchase_date')
            instance.updated_by = request.user
            instance.save()            
            messages.success(request, 'Portfolio updated successfully.')
            return redirect('portfolio:portfolio')  # Replace 'users-profile' with the appropriate URL name for your profile page
            # return redirect('portfolio')  # Redirect to the user's portfolio page


@login_required
def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolios, id=id)

    if request.method == 'GET':        
        form = DeletePortfolioForm(instance=portfolio)
        context = {
            'form': form,
            'metal_name': portfolio.metal.metal_name,
            'grade_name': portfolio.grade.grade_name,
            'productfamily_name': portfolio.product_family.productfamily_name,
            'product_name': portfolio.product.product_name,
            'metal_quantity': portfolio.metal_quantity,
            'ounces': portfolio.ounces,
            'head_title': "Delete Metals | Priority Gold Plus"
        }
        return render(request, 'delete_portfolio.html', context)

    if request.method == 'POST':
        form = DeletePortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.is_deleted = True
            instance.updated_by = request.user
            instance.save()            
            messages.success(request, 'Portfolio updated successfully.')
            return redirect('portfolio:list_metals')  # Replace 'users-profile' with the appropriate URL name for your profile page
            # return redirect('portfolio')  # Redirect to the user's portfolio page


@login_required
def products_list(request):
    # Get the logged-in user
    user = request.user
    # Retrieve the Products
    products = Products.objects.all().order_by('product_name')
    if products.exists():
        products_data = []
        distinct_metals = []
        for product in products:
            # Check if the metal is not already in the distinct_metals list
            if product.metal not in distinct_metals:
                # Add the metal to the distinct_metals list
                distinct_metals.append(product.metal)

            metal = product.metal
            grade = product.grade

            # Get the latest product price for the product
            # latest_price = ProductPrices.objects.filter(sku=product.sku, metal_name = metal.metal_name, grade = grade.grade_name, is_active=True).latest('updated')
            latest_price = ProductPrices.objects.filter(sku=product.sku, is_active=True).latest('updated')
            if latest_price:            
                # Create a dictionary with product data
                product_entry = {
                    'product': product, 
                    'metal': product.metal, 
                    'grade': product.grade, 
                    'product_family': product.product_family, 
                    'sku':latest_price.sku, 
                    'product_name':latest_price.product_name, 
                    'metal_name':latest_price.metal_name, 
                    'productfamily_name':latest_price.productfamily_name, 
                    'assetclass_name':latest_price.assetclass_name, 
                    'ounces':latest_price.ounces, 
                    'cogs':latest_price.cogs, 
                    'bid':latest_price.bid, 
                    'ask':latest_price.ask, 
                    'base_ask':latest_price.base_ask, 
                    'cost_source':latest_price.cost_source, 
                    'base_currency':latest_price.base_currency, 
                    'description':latest_price.description, 
                    'retail_shipping':latest_price.retail_shipping, 
                    'wholesale_shipping':latest_price.wholesale_shipping, 
                    'is_active':latest_price.is_active, 
                    'created':latest_price.created, 
                    'price_updated':latest_price.updated.strftime("%m/%d/%Y %I:%M:%S %p"),
                    'product_updated':product.updated.strftime("%m/%d/%Y"),
                }
                #  Add the portfolio data to the list
                products_data.append(product_entry)
        

        context = {"head_title": "Edit Products | Priority Gold Plus",'products': products,'products_data': products_data,'distinct_metals': distinct_metals,}
        return render(request, 'product_list.html', context)
    else:
        # No data, render the add_metal.html template
        context = {"head_title": "Edit Products | Priority Gold Plus",}
        return render(request, 'product_list.html', context)


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    if request.method == 'POST':
        form = ProductUpdateForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('portfolio:products_list')  # Redirect to the list of products
        else:
            messages.error(request, 'Form is not valid. Please correct the errors below.')
            form = ProductUpdateForm(request.POST)
            context = {'form': form, 
                        'metal_name': product.metal.metal_name,
                        'grade_name': product.grade.grade_name,
                        'productfamily_name': product.product_family.productfamily_name,
                        'product_name': product.product_name,
                        'ounces': product.ounces,        
                        'product': product,
                       "head_title": "Edit Products | Priority Gold Plus"}
            return render(request, 'product_update.html', context)            
    else:
        form = ProductUpdateForm(instance=product)
    
    context = {
        'form': form,
        'metal_name': product.metal.metal_name,
        'grade_name': product.grade.grade_name,
        'productfamily_name': product.product_family.productfamily_name,
        'product_name': product.product_name,
        'ounces': product.ounces,        
        'product': product,
        "head_title": "Edit Products | Priority Gold Plus"
    }
    return render(request, 'product_update.html', context)


# Create your views here.
def portfolio_update(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Edit Metals | Priority Gold Plus"}
    return render(request, "edit_metals.html", context)

def portfolio(request):
    # page = PrivacyPolicy.objects.first()
    # data = {"head_title": "Privacy Policy | Priority Gold", "page": page}
    context = {"head_title": "Portfolio | Priority Gold Plus"}
    return render(request, "portfolio.html", context)
# return render(request, 'users/admin/edit_profile.html', context)