# - * - coding: utf - 8 -*-
from odoo import models, fields

class LibraryMember(models.Model):

    _name = 'library.members'
    _description = 'Library Members'

    name = fields.Char(string='Members', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    membership_date = fields.Date(string='Membership Date')
