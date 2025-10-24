# - * - coding: utf - 8 -*-

{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'author': 'Your Name',
    'category': 'Library',
    'website': 'https://www.aktivsoftware.com',
    'description': """Create a Library Management module in Odoo that includes two custom models, two separate
menus, and basic Odoo fields with list and form views.""",
    'depends': ['base','sale_management', 'stock', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'reports/ir_action_reports.xml',
        'reports/report_library_book_views.xml',
        'reports/report_libraray_data_inherited_views.xml',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_author_views.xml',
        'views/library_member_views.xml',
        'views/library_library_views.xml',
        'views/library_book_tag_views.xml',
        'views/library_menu_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
