# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Book(models.Model):

    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    publication_date = fields.Date(string='Publication Date')
    member_ids = fields.One2many(comodel_name='library.members',
                                 inverse_name='book_member_id',
                                 string='Members')
    author_ids = fields.Many2one(comodel_name='library.author',
                                 string='Authors')
    library_id = fields.Many2one(comodel_name='library.library', string='Library')
    library_location = fields.Char(string='Library Location',
                                   related = 'library_id.location',
                                   store=True)
    book_reference = fields.Char(string='Book Reference', store=True)

    @api.onchange('name','author_ids')
    def _onchange_book_reference(self):
        """
        define:_onchange_book_reference
        description: Book Title and Book author name is displayed and updated when
                     changes are made.
        params: name, author_ids
        returns: book_reference
        """
        for record in self:
            if record.name and record.author_ids:
                record.book_reference = f"{record.name} - {record.author_ids.name}"
            else:
                record.book_reference = ' '
