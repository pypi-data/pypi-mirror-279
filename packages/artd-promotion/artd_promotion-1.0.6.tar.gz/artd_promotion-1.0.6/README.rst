ArtD Promotion
==============
Art Promotion is a package that manage coupon codes.
----------------------------------------------------
1. Add to your INSTALLED_APPS setting like this:

.. code-block:: python

    INSTALLED_APPS = [
        'django-json-widget'
        'artd_location',
        'artd_partner',
        'artd_product',
        'artd_customer',
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
        python manage.py create_base_customer_groups