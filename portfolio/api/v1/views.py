from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from .serializers import GradesSerializer,ProductFamilySerializer,PortfolioSerializer,SummarizedMetalSerializer  # Import the serializer here
from rest_framework import status
from portfolio.models import *
from django.db import transaction
# import logging

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


# class GradesView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         grade_choices = [
#             {'value': choice[0], 'label': choice[1]} for choice in GRADE_CHOICES
#         ]
#         serializer = GradesSerializer(grade_choices, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductFamilyByMetalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        metal_id = self.request.query_params.get('metal_id')
        grade_id = self.request.query_params.get('grade_id')
        # metal_id = request.GET.get('metal_id')
        # grade_id = request.GET.get('grade_id')
        
        # products = Products.objects.filter(metal_id=metal_id,is_active=True)               
        products = Products.objects.filter(metal_id=metal_id, grade_id=grade_id, is_active=True)
        # products = Products.objects.filter(grade_id=grade_id, is_active=True)
        # Extract product family IDs from the products queryset
        productfamily_ids = products.values_list('product_family_id', flat=True)
        # Filter ProductFamilies based on the extracted product family IDs
        product_families = ProductFamilies.objects.filter(productfamily_id__in=productfamily_ids, is_active=True).order_by('productfamily_name')

        # product_families = ProductFamilies.objects.filter(is_active=True)
        serializer = ProductFamilySerializer(product_families, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AddPortfolioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        print(request.data)  # Print data to the console
        serializer = PortfolioSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                # , metal_value=request.data.acquisition_cost, sku=request.data.sku
                serializer.save(created_by=request.user, updated_by=request.user)
            return Response({"status": "Portfolio added successfully"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)  # Print validation errors to the console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdatePortfolioAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id')
            portfolio = Portfolios.objects.get(id=id)
        except Portfolios.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PortfolioSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save(updated_by=request.user)
            return Response({"status": "Portfolio updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
class DeletePortfolioAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        try:
            id = request.query_params.get('id')
            portfolio = Portfolios.objects.get(id=id)
        except Portfolios.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)
        
        portfolio.is_deleted = True
        portfolio.save()

        return Response({"status": "Portfolio deleted successfully"}, status=status.HTTP_200_OK)    
    

class GetUserPortfolioByMetalAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        metal_id = self.request.query_params.get('metal_id')
        user = request.user  # Get the currently authenticated user
        
        portfolios = Portfolios.objects.filter(created_by=user,metal_id=metal_id, is_deleted=False)
        
        # Serialize the portfolio data along with the ask rate
        serialized_portfolios = []        
        
        for portfolio in portfolios:
            product = portfolio.product        
            # product_family = portfolio.product_family
            metal = portfolio.metal
            grade = portfolio.grade
            latest_price = ProductPrices.objects.filter(sku=product.sku, metal_name = metal.metal_name, grade = grade.grade_name, is_active=True).latest('updated')
            # Calculate the current value
            factor_rate = product.factor_rate if product else 0.00
            ask_price = latest_price.ask if latest_price else 0.00
            metal_quantity = portfolio.metal_quantity
            acquisition_cost = portfolio.acquisition_cost
            current_value = (ask_price * metal_quantity) * factor_rate
            price_updated = latest_price.updated if latest_price else timezone.now()

            serialized_portfolio = PortfolioSerializer(portfolio).data  # Serialize the portfolio
            serialized_portfolio['factor_rate'] = factor_rate
            serialized_portfolio['ask'] = ask_price
            serialized_portfolio['current_value'] = current_value
            serialized_portfolio['difference_value'] = (current_value - acquisition_cost)
            serialized_portfolio['percentage_change'] = ((current_value - acquisition_cost)/ acquisition_cost) * 100
            serialized_portfolio['price_updated'] = price_updated

            serialized_portfolios.append(serialized_portfolio)
            
        # serializer = PortfolioSerializer(portfolios, many=True)
        return Response(serialized_portfolios, status=status.HTTP_200_OK)
        # return Response(serializer.data, status=status.HTTP_200_OK)
       

class MetalSummarizedDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Your existing code...
        user = request.user
        user_portfolios = Portfolios.objects.filter(created_by=user, is_deleted=False)

        
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
                # last_updated_date = last_updated.strftime("%m/%d/%Y")
                # Format last_updated in the desired format "MM/DD/YYYY HH:MM:SS AM/PM"
                purchase_date = pu_date.strftime("%m/%d/%Y")

            # Get the latest product price for the product
            latest_price = ProductPrices.objects.filter(sku=product.sku, metal_name = metal.metal_name, grade = grade.grade_name, is_active=True).latest('updated')

            # Calculate the acquisition value and current value
            acquisition_value =0.0000
            acquisition_value = portfolio.acquisition_cost
            ounces = 0.0000
            ounces = portfolio.ounces
            current_value = 0.0000  # Default current value
            metal_quantity = portfolio.metal_quantity
            factor_rate = product.factor_rate

            if latest_price:            
                metal_quantity = portfolio.metal_quantity
                cogs = latest_price.cogs
                bid = latest_price.bid
                ask = latest_price.ask
                base_ask = latest_price.base_ask
                cost_source = latest_price.cost_source
                last_updated = latest_price.updated
                # current_value = latest_price.ask * portfolio.metal_quantity
                current_value = ((ask * metal_quantity) * factor_rate)

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
                'ounces':ounces,
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

            # Add the portfolio data to the list
            portfolio_data.append(portfolio_entry)


        summarized_metal_data = {}

        for entry in portfolio_data:
            metal_name = entry['metal'].metal_name
            metal_id = entry['metal'].metal_id

            if metal_name not in summarized_metal_data:
                summarized_metal_data[metal_name] = {
                    'metal_id': metal_id,
                    'metal_name': metal_name,
                    'total_ounces': (entry['ounces'] * entry['metal_quantity']),
                    'total_metal_quantity': entry['metal_quantity'],
                    'total_acquisition_value': entry['acquisition_value'],
                    'total_current_value': entry['current_value'],
                    'total_difference_value': entry['difference_value'],
                }
            else:
                summarized_metal_data[metal_name]['total_ounces'] += entry['ounces']
                summarized_metal_data[metal_name]['total_metal_quantity'] += entry['metal_quantity']
                summarized_metal_data[metal_name]['total_acquisition_value'] += entry['acquisition_value']
                summarized_metal_data[metal_name]['total_current_value'] += entry['current_value']
                summarized_metal_data[metal_name]['total_difference_value'] += entry['difference_value']

        for metal_data in summarized_metal_data.values():
            metal_data['total_percentage_change'] = (
                (metal_data['total_difference_value'] / metal_data['total_acquisition_value']) * 100
            )
            # Round the values to zero decimal places
            metal_data['total_ounces'] = round(metal_data['total_ounces'], 4)
            metal_data['total_metal_quantity'] = round(metal_data['total_metal_quantity'], 0)
            metal_data['total_acquisition_value'] = round(metal_data['total_acquisition_value'], 0)
            metal_data['total_current_value'] = round(metal_data['total_current_value'], 0)
            metal_data['total_difference_value'] = round(metal_data['total_difference_value'], 0)

        # Serialize the list directly, without wrapping it in another dictionary
        # serializer = SummarizedMetalSerializer(summarized_metal_data, many=True)
        serializer = SummarizedMetalSerializer(summarized_metal_data.values(), many=True)
        return Response(serializer.data)
