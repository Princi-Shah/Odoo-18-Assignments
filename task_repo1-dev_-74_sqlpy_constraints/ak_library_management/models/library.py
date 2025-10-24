# -*- coding: utf-8 -*-
from odoo import models, fields

class Library(models.Model):
    _name = 'library.library'
    _description = 'Library Management'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    book_ids = fields.One2many(comodel_name='product.template',
                               inverse_name='library_id', string="Books")

    _sql_constraints = [('unique_name', 'unique (name)',
                         'Library name should be unique.'),
                        ('library_capacity', 'CHECK(capacity <= 10)',
                         'Capacity cannot exceed 10.')]
