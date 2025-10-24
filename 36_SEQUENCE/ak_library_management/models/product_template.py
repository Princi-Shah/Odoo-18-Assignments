# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string='Is Library Book')
    author = fields.Char(string='Author')  # renamed for clarity
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Published Date')
    pages = fields.Integer(string='Pages')
    isbn_number = fields.Char(string="ISBN Number")
    status = fields.Selection([ ("available", "Available"),
                                ("borrowed", "Borrowed"),
                                ("reserved", "Reserved")], string="Status",
                              default="available")

    def action_available(self):
        self.status = 'available'

    def action_borrowed(self):
        self.status = 'borrowed'

    def action_reserved(self):
        self.status = 'reserved'

    def create(self, vals):
        """
        define: create
        description: it generates the dynamic sequence as product is created
        params: vals
        returns: res
        """
        res = super(ProductTemplate, self).create(vals)
        if res.is_library_book:
            # generate book reference sequence
            res.default_code = self.env['ir.sequence'].next_by_code('book.reference')
        return res
