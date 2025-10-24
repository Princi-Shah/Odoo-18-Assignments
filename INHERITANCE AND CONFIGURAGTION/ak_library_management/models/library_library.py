# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Library(models.Model):

    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    notes = fields.Text(string='Notes')
    book_ids = fields.Many2many('product.template',
                                domain="[('is_library_book', '=', True)]")
