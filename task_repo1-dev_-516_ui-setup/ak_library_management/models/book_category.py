# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookCategory(models.Model):
    """
    Class method for book category including many2one relational field for books
    """

    _name = 'library.book.category'
    _description = 'Book Category'
    _rec_name = 'name'

    name = fields.Char(string='Book Category', required=True)
    book_id = fields.Many2one('library.book', string='Book')
