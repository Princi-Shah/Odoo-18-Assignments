# - * - coding: utf - 8 -*-
from odoo import fields, models, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    book_state = fields.Selection([('available', 'Available'),
                                   ('borrowed', 'Borrowed'),
                                   ('reserved', 'Reserved')], string='Book Status',
                                  default='available', store=True)
    library_id = fields.Many2one(comodel_name='library.library', string='Library')
    author_ids = fields.One2many(comodel_name='library.author', inverse_name='book_member_id',
                                 string='Authors')
    date_release = fields.Date(string='Publication Date')
    library_location = fields.Char(string='Library Location', related='library_id.location',
                                   store=True)

    def action_mark_borrowed(self):
        """
        define: action_mark_borrowed
        description: function to change book status to borrowed
        returns: None
        """
        for record in self:
            record.book_state = 'borrowed'

    def action_mark_available(self):
        """
        define: action_mark_available
        description: function to change book status to available
        returns: None
        """
        for record in self:
            record.book_state = 'available'

    def action_return_book(self):
        """
        define: action_return_book
        description: function to change book status to available when book returned
        returns: None
        """
        for record in self:
            record.book_state = 'available'
