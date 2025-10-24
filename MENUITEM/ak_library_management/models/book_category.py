# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookCategory(models.Model):
    """
    Class method for book category including many2one relational field for books
    """
    _name = 'library.book.category'
    _description = 'Book Category'
    _rec_name = 'name'

    name = fields.Char(string='Category', required=True)
    # relational field for book category to tags
    tag_ids = fields.Many2many('library.book.tag', string='Tags')
