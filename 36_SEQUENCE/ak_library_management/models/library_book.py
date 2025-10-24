# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class Book(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    date_release = fields.Date(string='Publication Date')
    author = fields.Char(string='Authors')
    library_id = fields.Many2one(comodel_name='library.library', string='Library')
    isbn_number = fields.Char(string='ISBN')
    book_state = fields.Selection(
        [('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('reserved', 'Reserved')],
        string='Book Status',
        default='available',
        store=True
    )
    library_location = fields.Char(string='Library Location',
                                   related='library_id.location',store=True)
    book_reference = fields.Char(
        string='Book Reference',
        readonly=True,
        copy=False,
        index=True
    )

    @api.model
    def create(self, vals):
        """
        define: create
        description: it generates the dynamic sequence as library product is created
        params: vals
        returns: book_reference
        """
        if not vals.get("book_reference"):
            vals["book_reference"] = (
                self.env["ir.sequence"].next_by_code("book.reference") or _("New")
            )
        return super(Book, self).create(vals)

    def action_mark_borrowed(self):
        """
        define: action_mark_borrowed
        description: It changes the book state as per the action performed.
        params: self
        returns: book_state
        """
        self.write({"book_state": "borrowed"})

    def action_mark_available(self):
        """
        define: def action_mark_available
        description: It changes the book state as per the action performed.
        params: self
        returns: book_state
        """
        self.write({"book_state": "available"})

    def action_return_book(self):
        """
        define: action_return_book
        description: It changes the book state as per the action performed.
        params: self
        returns: book_state
        """
        self.write({"book_state": "available"})
