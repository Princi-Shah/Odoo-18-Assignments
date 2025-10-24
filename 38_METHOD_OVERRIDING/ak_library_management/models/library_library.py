    # - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Library(models.Model):

    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    notes = fields.Text(string='Notes')
    # relational field for library and books
    book_ids = fields.Many2many(comodel_name='product.template',
                                string='Books in Library',
                                domain="[('is_library_book', '=', True)]")
    # Applying compute method to calculate the number of books entered
    book_count = fields.Integer(string='Book Count',
                                compute='_compute_book_count',
                                store=True)
    capacity_status = fields.Char(string='Capacity Status',
                                  compute='_compute_capacity_status',
                                  store=True)
    # Compute method for borrowed book count to show message
    borrowed_book_count = fields.Integer(string='Borrowed Books',
                                         compute='_compute_borrowed_book_count')

    @api.depends('book_ids')
    def _compute_book_count(self):
        """
        define: _compute_book_count
        description: function helps perform the book count according to the library.
        returns: None
        """
        for record in self:
            record.book_count = len(record.book_ids)

    @api.depends('book_count', 'capacity')
    def _compute_capacity_status(self):
        """
        define: _compute_capacity_status
        description: function helps perform the check when library has the capacity
                     check and showing the assigned value according to the capacity.
        returns: None
        """
        for record in self:
            if record.capacity == 0:
                record.capacity_status = 'Available'
            else:
                ratio = record.book_count / record.capacity
                if ratio < 0.8:
                    record.capacity_status = 'Normal'
                elif ratio < 1.0:
                    record.capacity_status = 'Warning'
                else:
                    record.capacity_status = 'Full'

    @api.depends('book_ids.available')
    def _compute_borrowed_book_count(self):
        """
        define: _compute_borrowed_book_count
        description: function helps perform the count method on number of books borrowed.
        returns: None
        """
        for library in self:
            library.borrowed_book_count = len(library.book_ids.filtered(
                lambda book: book.book_state == 'borrowed'))
