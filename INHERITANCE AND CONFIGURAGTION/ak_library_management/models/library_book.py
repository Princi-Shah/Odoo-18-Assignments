# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Book(models.Model):

    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    publication_date = fields.Date(string='Publication Date')
    member_id = fields.Many2one('library.members', string='Members')
    author_ids = fields.Many2many('library.author', string='Authors')
    library_id = fields.Many2one('library.library', string='Library')
    isbn_number = fields.Char(string='ISBN')
    book_description = fields.Text(string='Book Description')
    book_reference = fields.Char(string='Book Reference', store=True)

    @api.onchange('name', 'author_ids')
    def _onchange_book_reference(self):
        """
        define: _onchange_book_reference
        description: In this method it is fetching the value from the book name and
                     author name to display them together in a particular format.
        params: name, author_ids
        returns: value in a "-" formate into book_reference
        """
        for record in self:
            if record.name and record.author_ids:
                authors = ', '.join(record.author_ids.mapped('name'))
                record.book_reference = f"{record.name} - {authors}"
            else:
                record.book_reference = ''
