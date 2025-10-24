# - * - coding: utf - 8 -*-
from odoo import fields, models

class ReserveBookWizard(models.TransientModel):
    _name = 'reserve.book.wizard'
    _description = 'Reserve Book Wizard'

    customer_id = fields.Many2one('res.partner',
                                  string='Customer',
                                  required=True,
                                  domain=[('can_reserve_books', '=', True)])
    book_id = fields.Many2one('product.template',
                              string='Book',
                              readonly=True)
    expected_pickup_date = fields.Datetime(string='Expected Pickup Date', required=True)

    def action_confirm(self):
        """
        define: action_confirm
        description: function helps perform the confirm method on confirm button inside
                    wizard.
        returns: None
        """
        self.env['book.reservation'].create({
            'customer_id': self.customer_id.id,
            'book_id': self.book_id.id,
            'expected_pickup_date': self.expected_pickup_date,
            'state': 'reserved',
        })
        return {'type': 'ir.actions.act_window_close'}
