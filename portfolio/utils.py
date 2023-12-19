import requests
from .models import *


def fetch_metals_from_api():
    url = "https://prioritygold.nfusioncatalog.com/service/settings/metals?token=a2f31b0a-dc9d-4b59-9ce9-42d4b32144e2"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if isinstance(data, list):
            metals_list = data  # The response is a list of metals
        elif isinstance(data, dict) and 'results' in data:
            metals_list = data['results']  # Extract the list of metals from the 'results' key
        else:
            raise ValueError("Invalid response format")

        return metals_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metals from API: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None

def save_metals_to_database():
    metals = fetch_metals_from_api()
    if metals is not None:
        for data in metals:
            uid = User.objects.get(pk=1)
            metal_id = data['Id']
            defaults = {
                'metal_name': data['Name'],
                # 'is_active': True,
                'created_by': uid,
                'updated_by': uid,
                # 'updated_on': timezone.now(),
            }
            metal, created = Metals.objects.update_or_create(metal_id=metal_id, defaults=defaults)

def fetch_asset_classes_from_api():
    url = "https://prioritygold.nfusioncatalog.com/service/settings/assetclasses?token=a2f31b0a-dc9d-4b59-9ce9-42d4b32144e2"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if isinstance(data, list):
            metals_list = data  # The response is a list of metals
        elif isinstance(data, dict) and 'results' in data:
            metals_list = data['results']  # Extract the list of metals from the 'results' key
        else:
            raise ValueError("Invalid response format")

        return metals_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching asset classes from API: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None
    
def save_asset_classes_to_database():
    asset_classes = fetch_asset_classes_from_api()
    if asset_classes is not None:
        for data in asset_classes:
            uid = User.objects.get(pk=1)
            assetclass_id = data['Id']
            defaults = {
                'assetclass_name': data['Name'],
                'percent_markup': data.get('PercentMarkup', 0.00),
                # 'is_active': True,
                'created_by': uid,
                'updated_by': uid,
                # 'updated_on': timezone.now(),
            }
            assetclass, created = AssetClasses.objects.update_or_create(assetclass_id=assetclass_id, defaults=defaults)


def fetch_product_families_from_api():
    url = "https://prioritygold.nfusioncatalog.com/service/settings/productfamilies?token=a2f31b0a-dc9d-4b59-9ce9-42d4b32144e2"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if isinstance(data, list):
            product_families_list = data  # The response is a list of metals
        elif isinstance(data, dict) and 'results' in data:
            product_families_list = data['results']  # Extract the list of metals from the 'results' key
        else:
            raise ValueError("Invalid response format")

        return product_families_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metals from Product Families API: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None
    

def save_product_families_to_database():
    product_families_list = fetch_product_families_from_api()
    if product_families_list is not None:
        for data in product_families_list:
            uid = User.objects.get(pk=1)
            parent_id = data.get('ParentId', '')  # Use get() with default value ''
            assetclass_id = data.get('AssetClassId', '')  # Use get() with default value ''
            assetclass = AssetClasses.objects.get(assetclass_id=assetclass_id)
            productfamily_id = data['Id']

            defaults = {
                'productfamily_name': data['Name'],
                # 'assetclass_id': assetclass_id,
                'assetclass': assetclass,
                'parent_id': parent_id,
                # 'is_active': True,
                'created_by': uid,
                'updated_by': uid,
                # 'updated_on': timezone.now(),
            }
            product_family, created = ProductFamilies.objects.update_or_create(productfamily_id=productfamily_id, defaults=defaults)

def fetch_products_from_api():
    url = "https://prioritygold.nfusioncatalog.com/service/settings/products?token=a2f31b0a-dc9d-4b59-9ce9-42d4b32144e2"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if isinstance(data, list):
            metals_list = data  # The response is a list of metals
        elif isinstance(data, dict) and 'results' in data:
            metals_list = data['results']  # Extract the list of metals from the 'results' key
        else:
            raise ValueError("Invalid response format")

        return metals_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metals from Products API: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None
    
def save_products_to_database():
    products_list = fetch_products_from_api()
    if products_list is not None:
        for data in products_list:
            uid = User.objects.get(pk=1)
            metal_id = data.get('MetalId', '')  # Use get() with default value ''
            metal = Metals.objects.get(metal_id=metal_id)
            productfamily_id = data.get('ProductFamilyId', '')  # Use get() with default value ''
            productfamily = ProductFamilies.objects.get(productfamily_id=productfamily_id)

            grade = data.get('Grade', '').strip()  # Use get() with default value '' and strip() to remove whitespace
            metal_grade = Grades.objects.get(grade_name=grade)
            
            sku = data['Sku']
            defaults = { 
                'product_name': data['Name'],
                'product_description': data.get('Description', ''),
                'product_notes': data.get('Notes', ''),
                'metal': metal,
                'ounces': data.get('Ounces', 0.00),
                'product_family': productfamily,
                'grade': metal_grade, #data.get('Grade', ''),
                'commission': data.get('Commission', 0.00),
                'url': data.get('Url', '#'),
                'thumbnail_url': data.get('ThumbnailUrl', '#'),
                'image_url': data.get('ImageUrl', '#'),
                'base_currency': data['BaseCurrency'],
                'base_ask': data.get('BaseAsk', 0.00),
                'base_bid': data.get('BaseBid', 0.00),
                'cost_source': data['CostSource'],
                'bid_source': data['BidSource'],
                'cogs_percent': data.get('CogsPercent', 0.00),
                'cogs_dollar': data.get('CogsDollar', 0.00),
                'grading_fee': data.get('GradingFee', 0.00),
                'fixed_markup_ask': data.get('FixedMarkupAsk', 0.00),
                'percent_markup_ask': data.get('PercentMarkupAsk', 0.00),
                'fixed_markup_bid': data.get('FixedMarkupBid', 0.00),
                'percent_markup_bid': data.get('PercentMarkupBid', 0.00),
                'fixed_markup_ask_wholesale': data.get('FixedMarkupAskWholesale', 0.00),
                'percent_markup_ask_wholesale': data.get('PercentMarkupAskWholesale', 0.00),
                'fixed_markup_bid_wholesale': data.get('FixedMarkupBidWholesale', 0.00),
                'percent_markup_bid_wholesale': data.get('PercentMarkupBidWholesale', 0.00),

                'wholesale_notes': data.get('WholesaleNotes', ''),
                'track_inventory': data['TrackInventory'],
                'retail_shipping': data.get('RetailShipping', 0.00),
                'retail_shipping_notes': data.get('RetailShippingNotes', ''),
                'wholesale_shipping': data.get('WholesaleShipping', 0.00),
                'wholesale_shipping_notes': data.get('WholesaleShippingNotes', ''),
                # 'is_active': True,
                'created_by': uid,
                'updated_by': uid,
                # 'updated_on': timezone.now(),
            }

            product, created = Products.objects.update_or_create(sku=sku, metal_id=metal_id,product_family_id=productfamily_id, defaults=defaults)


def fetch_product_prices_from_api():
    url = "https://prioritygold.nfusioncatalog.com/service/price/all?currency=CAD&withretailtiers=true&withwholesaletiers=true&withCost=true&token=a2f31b0a-dc9d-4b59-9ce9-42d4b32144e2&shippingInAsk=true"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        data = response.json()
        if isinstance(data, list):
            metals_list = data  # The response is a list of prices
        elif isinstance(data, dict) and 'results' in data:
            metals_list = data['results']  # Extract the list of prices from the 'results' key
        else:
            raise ValueError("Invalid response format")

        return metals_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching prices from Product Prices/all API: {e}")
        return None
    except ValueError as e:
        print(f"Invalid response format: {e}")
        return None
    
def save_product_prices_to_database():
    price_list = fetch_product_prices_from_api()
    if price_list is not None:
        for data in price_list:
            uid = User.objects.get(pk=1)
            sku = data.get('SKU', '')
            metal_name = data.get('Metal', '')
            productfamily_name = data.get('ProductFamily', '')
            assetclass_name = data.get('AssetClass', '')
            grade = data.get('Grade', '')
            ounces = data.get('Ounces', 0.00)
            cogs = data.get('Cogs', 0.00)
            bid = data.get('Bid', 0.00)
            ask = data.get('Ask', 0.00)
            base_ask = data.get('BaseAsk', 0.00)
            cost_source = data['CostSource']
            base_currency = data['BaseCurrency']
            retail_shipping = data.get('RetailShipping', 0.00)
            wholesale_shipping = data.get('WholesaleShipping', 0.00)                        
            
            defaults = { 
                'product_name': data['Name'],                
                # 'metal_name': data.get('Metal', ''),
                # 'productfamily_name': data.get('ProductFamily', ''),
                # 'assetclass_name': data.get('AssetClass', ''),
                # 'grade': data.get('Grade', ''),
                # 'ounces': data.get('Ounces', 0.00),
                # 'cogs': data.get('Cogs', 0.00),
                # 'bid': data.get('Bid', 0.00),
                # 'ask': data.get('Ask', 0.00),
                # 'base_ask': data.get('BaseAsk', 0.00),
                # 'cost_source': data['CostSource'],
                # 'base_currency': data['BaseCurrency'],
                'description': data.get('Description', ''),
                # 'retail_shipping': data.get('RetailShipping', 0.00),
                # 'wholesale_shipping': data.get('WholesaleShipping', 0.00),
                # 'is_active': True,
                'created_by': uid,
                'updated_by': uid,
                # 'updated_on': timezone.now(),
            }

            product_price, created = ProductPrices.objects.update_or_create(sku=sku, metal_name=metal_name, productfamily_name=productfamily_name,assetclass_name=assetclass_name, 
                                                                            grade = grade, ounces = ounces, cogs = cogs, bid = bid, ask = ask, base_ask = base_ask,
                                                                            cost_source = cost_source, base_currency = base_currency, retail_shipping = retail_shipping,
                                                                            wholesale_shipping = wholesale_shipping, defaults=defaults)
            