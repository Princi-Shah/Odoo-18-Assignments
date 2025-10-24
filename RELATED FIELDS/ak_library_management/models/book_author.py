# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookAuthor(models.Model):

    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Author', required=True)
    book_member_id = fields.Many2one(comodel_name='library.book', string='Book')
