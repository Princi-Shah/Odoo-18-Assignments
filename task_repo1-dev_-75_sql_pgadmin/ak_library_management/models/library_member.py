# - * - coding: utf - 8 -*-
from odoo import models, fields

class LibraryMember(models.Model):

    _name = 'library.members'
    _description = 'Library Members'

    name = fields.Char(string='Members', required=True)
    book_member_id = fields.One2many(comodel_name='library.book',
                                     inverse_name='member_id',
                                     string='Member')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    membership_date = fields.Date(string='Membership Date')
