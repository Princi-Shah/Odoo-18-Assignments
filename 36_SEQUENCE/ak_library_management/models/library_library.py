# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Library(models.Model):
    _name = 'library.library'
    _description = 'Library'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    notes = fields.Text(string='Notes')
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='library_id',
                               string='Books')
    book_count = fields.Integer(string='Book Count', compute='_compute_book_count',
                                store=True)
    borrowed_book_count = fields.Integer(string='Borrowed Books',
                                         compute='_compute_book_count', store=True)
    capacity_status = fields.Char(string='Capacity Status',
                                  compute='_compute_capacity_status', store=True)

    @api.depends('book_ids', 'book_ids.book_state')
    def _compute_book_count(self):
        """
        define: _compute_book_count
        description: counts the number of books in the library.
        params: book_ids, book_ids.book_state
        returns: book_state
        """
        for record in self:
            record.book_count = len(record.book_ids)
            record.borrowed_book_count = len(
                record.book_ids.filtered(lambda b: b.book_state == 'borrowed')
            )

    @api.depends('book_count', 'capacity')
    def _compute_capacity_status(self):
        """
        define: _compute_capacity_status
        description: returns the state of capacity inside library according to the books
                     count.
        params: book_count, capacity
        returns: capacity
        """
        for record in self:
            if not record.capacity:
                record.capacity_status = 'Available'
            else:
                ratio = record.book_count / record.capacity
                if ratio < 0.8:
                    record.capacity_status = 'Normal'
                elif ratio < 1.0:
                    record.capacity_status = 'Warning'
                else:
                    record.capacity_status = 'Full'

    def action_view_book_borrow(self):
        """
        define: action_view_book_borrow
        description: It's an action function which can be written inside py file
                    as well as xml side what it does is that in py side it returns value
                    for particular domain condition passed where if want to apply filter
                    than also it is possible
        params: self
        returns: type,res_model,domain,name,view_mode
        """
        return {
            "type": "ir.actions.act_window",
            "res_model": "library.book",
            "domain": [('book_state', '=', 'borrowed'), ('library_id', '=', self.id)],
            "name": "Borrowed Books",
            "view_mode": "list,form",
        }
