# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Book(models.Model):

    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char(string='Title', required=True)
    date_release = fields.Date(string='Publication Date')
    member_ids = fields.One2many(comodel_name='library.members',
                                 inverse_name='book_member_id', string='Members')
    author_ids = fields.One2many(comodel_name='library.author',
                                 inverse_name='book_member_id', string='Authors')
    category_id = fields.Many2one(comodel_name='library.book.category',
                                  string='Category')
    library_id = fields.Many2one(comodel_name='library.library', string='Library')
    tag_ids = fields.Many2many(comodel_name='library.book.tag',
                               related='category_id.tag_ids',string='Tags')
    isbn_number = fields.Char(string='ISBN')
    book_description = fields.Text(string='Book Description')
    book_state = fields.Selection([('available', 'Available'),
                                   ('borrowed', 'Borrowed'),
                                   ('reserved', 'Reserved')], string='Book Status',
                                  default='available',
                                  compute='_compute_book_state',
                                  store=True)
    library_location = fields.Char(string='Library Location',
                                   related='library_id.location', store=True)
    book_reference = fields.Char(string='Book Reference', store=True)

    @api.depends('member_ids')
    def _compute_book_state(self):
        """
        define: _compute_book_state
        description: function helps perform the change of book state when action
                     performed.
        returns: None
        """
        for record in self:
            if record.member_ids:
                record.book_state = 'borrowed'
            else:
                record.book_state = 'available'

    @api.onchange('name', 'author_ids')
    def _onchange_book_reference(self):
        """
        define: _onchange_book_reference
        description: function helps fetch the book name and author name to print inside
                     the assigned field.
        returns: None
        """
        for record in self:
            if record.name and record.author_ids:
                authors = ', '.join(record.author_ids.mapped('name'))
                record.book_reference = f"{record.name} - {authors}"
            else:
                record.book_reference = ''

    def action_mark_borrowed(self):
        """
        define: action_mark_borrowed
        description: function helps perform the state change to borrowed when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.book_state = 'borrowed'

    def action_mark_available(self):
        """
        define: action_mark_available
        description: function helps perform the state change to available when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.book_state = 'available'

    def action_return_book(self):
        """
        define: action_return_book
        description: function helps perform the state change to available when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.book_state = 'available'
