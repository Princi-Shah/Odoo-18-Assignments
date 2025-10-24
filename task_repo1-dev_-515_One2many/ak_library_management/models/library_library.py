# - * - coding: utf - 8 -*-
from odoo import models, fields

class Library(models.Model):

    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Library Name', required=True)
    location = fields.Char(string='Library Location', required=True)
    capacity = fields.Integer(string='Library Capacity', required=True)
    notes = fields.Text(string='Library Notes')
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='library_id',
                               string='Books in Library')
