{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'author': 'Your Name',
    'category': 'Library',
    'website': 'https://www.aktivsoftware.com',
    'description': """Create a Library Management module in Odoo that includes two custom models, two separate
menus, and basic Odoo fields with list and form views.""",
    'depends': ['base','web'],
    'data': [
        'security/ir.model.access.csv',
        'views/library_book_views.xml',
        'views/library_book_category_views.xml',
        'views/library_author_views.xml',
        'views/library_member_views.xml',
        'views/library_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
