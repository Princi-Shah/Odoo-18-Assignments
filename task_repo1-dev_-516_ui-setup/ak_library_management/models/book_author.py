# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookAuthor(models.Model):
    """
    Class method for author details including Many2one relational field for books
    """
    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Author', required=True)
    book_member_id = fields.Many2one('library.book', string='Book')
