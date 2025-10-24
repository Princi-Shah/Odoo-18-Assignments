# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Library(models.Model):

    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    notes = fields.Text(string='Notes')

    book_ids = fields.One2many('product.template', 'library_id', string='Books in Library')

    book_count = fields.Integer(string='Book Count',
                                compute='_compute_book_count',
                                store=True)
    capacity_status = fields.Char(string='Capacity Status',
                                  compute='_compute_capacity_status',
                                  store=True)

    borrowed_book_count = fields.Integer(string='Borrowed Books',
                                         compute='_compute_borrowed_book_count',
                                         default=0)

    @api.depends('book_ids')
    def _compute_book_count(self):
        """
        define: _compute_book_count
        description: function helps calculate the number of books in library
        returns: None
        """
        for record in self:
            record.book_count = len(record.book_ids)
            print(f"the library name: {Library.name}: the available book count{Library.book_count}")

    @api.depends('book_count', 'capacity')
    def _compute_capacity_status(self):
        """
        define: _compute_capacity_status
        description: function helps calculate the capacity status and perform criteria based message in the library view
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

    @api.depends('book_ids.book_state')
    def _compute_borrowed_book_count(self):
        """
        define: _compute_borrowed_book_count
        description: function helps calculate the number of borrowed books in library
        returns: None
        """
        for library in self:
            library.borrowed_book_count = len(
                library.book_ids.filtered(lambda book: book.book_state == 'borrowed'))

    def action_get_borrowed_count(self):
        """
        define: action_get_borrowed_count
        description: calculates the borrowed count of books in library
        returns: object of the button
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Borrowed Books',
            'res_model': 'product.template',
            'view_mode': 'list,form',
            'domain': [('library_id', '=', self.id), ('book_state', '=', 'borrowed')],
            'context': dict(self.env.context, default_library_id=self.id),
        }
