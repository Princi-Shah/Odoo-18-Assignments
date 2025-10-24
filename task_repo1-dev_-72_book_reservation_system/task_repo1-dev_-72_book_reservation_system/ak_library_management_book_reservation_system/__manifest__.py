# - * - coding: utf - 8 -*-
{
    'name': 'Book Reservation System',
    'version': '18.0.1.0.1',
    'author': 'Your Name',
    'category': 'Library',
    'website': 'https://www.aktivsoftware.com',
    'description': """Book Reservation System""",
    'depends': ['base', 'product', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/book_reservation_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'wizards/reserve_book_wizard.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
