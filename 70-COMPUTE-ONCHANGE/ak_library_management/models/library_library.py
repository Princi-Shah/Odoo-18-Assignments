# - * - coding: utf - 8 -*-
from odoo import models, fields, api

class Library(models.Model):

    _name = 'library.library'
    _description = 'Different Libraries'

    name = fields.Char(string='Library Name', required=True)
    location = fields.Char(string='Library Location', required=True)
    capacity = fields.Integer(string='Library Capacity', required=True)
    book_ids = fields.One2many(comodel_name='library.book', inverse_name='library_id',
                               string='Books in Library')
    book_count = fields.Integer(string='Book Count', compute='_compute_book_count', store=True)
    capacity_status = fields.Char(string='Capacity Status', compute='_compute_capacity_status', store=True)

    @api.depends('book_ids')
    def _compute_book_count(self):
        """
        define:_compute_book_count
        description: Book count according to books present in the library.
        params: book_ids
        returns: book_count
        """
        for record in self:
            record.book_count = len(record.book_ids)

    @api.depends('book_ids', 'capacity')
    def _compute_capacity_status(self):
        """
        define:_compute_capacity_status
        description: Book capacity status according to books present in the library.
        params: book_ids, capacity
        returns: capacity_status
        """
        for record in self:
            ratio = record.book_count / record.capacity
            if ratio < 0.8:
                record.capacity_status = 'Normal'
            elif (ratio >= 0.8) and (ratio < 1.0):
                record.capacity_status = 'Warning'
            else:
                record.capacity_status = 'Full'
