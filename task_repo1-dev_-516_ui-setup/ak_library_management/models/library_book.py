# - * - coding: utf - 8 -*-
from odoo import models, fields

class Book(models.Model):
    """
    Class method for book including :
    1) one2many relational field for members
    2) many2many relational field for authors
    """

    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    date_release = fields.Date(string='Publication Date')
    member_ids = fields.One2many('library.members', 'book_member_id', string='Members')
    author_ids = fields.Many2many('library.author', string='Authors')
    category_ids = fields.One2many('library.book.category', 'book_id', string='Category')
    isbn_number = fields.Char(string='ISBN')
    book_description = fields.Text(string='Book Description')
    book_state = fields.Selection([('borrowed', 'Borrowed'),('available', 'Available')], string='Book Status')
