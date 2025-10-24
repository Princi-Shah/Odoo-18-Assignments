# - * - coding: utf - 8 -*-
from odoo import models, fields

class LibraryMember(models.Model):
    """
    Class method for members including :
    1) many2one relational field for book
    """
    _name = 'library.members'
    _description = 'Library Members'

    name = fields.Char(string='Members', required=True)
    book_member_id = fields.Many2one('library.book', string='Book')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    membership_date = fields.Date(string='Membership Date')
