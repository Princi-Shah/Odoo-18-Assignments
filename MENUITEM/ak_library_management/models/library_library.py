# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Library(models.Model):
    """
    Library model holds information about a physical library.
    One library can have multiple books
    """
    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    notes = fields.Text(string='Notes')
    # relational field for library and books
    book_ids = fields.One2many('library.book', 'library_id', string='Books in Library')

    # Applying compute method to calculate the number of books entered
    book_count = fields.Integer(string='Book Count', compute='_compute_book_count', store=True)
    capacity_status = fields.Char(string='Capacity Status', compute='_compute_capacity_status', store=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        """
        function helps calculate the number of books in library
        """
        for record in self:
            record.book_count = len(record.book_ids)
            print(f"the library name: {Library.name}: the available book count{Library.book_count}")

    @api.depends('book_count', 'capacity')
    def _compute_capacity_status(self):
        """
        function helps calculate the capacity status and perform criteria based message in the library view
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