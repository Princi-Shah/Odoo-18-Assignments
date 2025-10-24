# -*- coding: utf-8 -*-
{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'author': 'Your Name',
    'category': 'Library',
    'website': 'https://www.aktivsoftware.com',
    'description': """Create a Library Management module in Odoo that includes sql contraints used in models.""",
    'depends': ['base', 'product', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_views.xml',
        'views/product_template_views.xml',
        'views/res_users_views.xml',
        'views/library_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
