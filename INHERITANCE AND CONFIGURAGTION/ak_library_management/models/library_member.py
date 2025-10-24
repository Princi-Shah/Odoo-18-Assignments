# - * - coding: utf - 8 -*-
from odoo import models, fields

class LibraryMember(models.Model):

    _name = 'library.members'
    _description = 'Library Members'

    name = fields.Char(string='Members', required=True)
    borrowed_book_ids = fields.One2many('library.book','member_id', string='Borrowed Books')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    membership_date = fields.Date(string='Membership Date', required=True)
