# -*- coding: utf-8 -*-
{
    "name": "Purchase Extension",
    "summary": "Purchase Extension for Global Discount",
    "description": """Purchase Extension for Global Discount""",
    "author": "Htet Aung Shane",
    "sequence": "1",
    "website": "https://samplewebsite.com",
    "category": "Customizations",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "account",
        "purchase",
    ],
    # always loaded
    "data": [
        # views
        "views/purchase_order.xml",
    ],
    "application": True,
    "license": "LGPL-3",
    # 'assets': {
    #     'web.assets_backend': [
    #         'purchase_ext/static/src/components/**/*',
    #     ],
    # }
}
