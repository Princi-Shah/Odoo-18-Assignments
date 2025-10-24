# - * - coding: utf - 8 -*-
from odoo import models, fields

class BookAuthor(models.Model):

    _name = 'library.author'
    _description = 'Library Author'

    name = fields.Char(string='Author', required=True)
