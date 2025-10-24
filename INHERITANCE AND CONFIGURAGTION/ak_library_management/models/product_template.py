# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string='Is Library Book',default=False)
    author_ids = fields.Many2many('library.author', string='Authors')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    borrowed_book_count = fields.Integer(
        string='Borrowed Book Count',
        compute='_compute_borrowed_book_count'
    )
