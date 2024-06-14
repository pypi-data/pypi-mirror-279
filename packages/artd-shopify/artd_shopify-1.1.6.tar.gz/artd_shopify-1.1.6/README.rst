ArtD Shopify
============
ArtD Shopify is a package that connects with a store developed in Shopify and extracts products, their variants, prices, stock and images and other data.
---------------------------------------------------------------------------------------------------------------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_product',
        'artd_product_price',
        'artd_stock',
        'artd_shopify',
    ]
2. Run the migration commands:
   
.. code-block::
    
        python manage.py makemigrations
        python manage.py migrate


3. Run the seeder data:
   
.. code-block::

        python manage.py create_countries
        python manage.py create_colombian_regions
        python manage.py create_colombian_cities
        python manage.py create_taxes

4. After you've installed the migrations and set up login details, you can import the information from Shopify
   
.. code-block::
        
        python manage.py import_shopify_product <<partner_slug>>