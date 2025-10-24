# - * - coding: utf - 8 -*-
from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    reservation_book_count = fields.Integer(compute='compute_reservation_book_count')

    def compute_reservation_book_count(self):
        """
        define: compute_reservation_book_count
        description: function helps calculate the reservation book count
        returns: None
        """
        for book in self:
            book.reservation_book_count = self.env['book.reservation'].search_count(
                [('book_id', '=', book.id)])

    def action_view_reservations(self):
        """
        define: action_view_reservations
        description: function helps view data of reserved books details in list and
                    form view.
        returns: None
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reservations',
            'view_mode': 'list,form',
            'res_model': 'book.reservation',
            'domain': [('book_id', '=', self.id)],
        }

    def action_open_reservation_wizard(self):
        """
        define: action_open_reservation_wizard
        description: function helps open a reservation wizard
        returns: None
        """
        return {
            'name': 'Reserve Book',
            'type': 'ir.actions.act_window',
            'res_model': 'reserve.book.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_book_id': self.id}
        }
