# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookCategory(models.Model):

    _name = 'library.book.category'
    _description = 'Book Category'
    _rec_name = 'name'

    name = fields.Char(string='Book Category', required=True)
