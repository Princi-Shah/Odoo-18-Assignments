# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookAuthor(models.Model):

    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Author', required=True)
    book_author_id = fields.One2many(comodel_name='library.book',
                                     inverse_name='author_id',
                                     string='Authors')
