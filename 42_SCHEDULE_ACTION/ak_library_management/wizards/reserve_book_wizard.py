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
                              string='Book')
    expected_pickup_date = fields.Datetime(string='Expected Pickup Date')
    reservation_id = fields.Many2one('book.reservation', string="Reservation")

    def action_pick_up(self):
        """
        define: action_pick_up
        description: function helps perform the picked up method on call of pick up
                     button inside wizard.
        returns: window action
        """

        self.ensure_one()
        if self.reservation_id:
            self.reservation_id.write({
                'state': 'picked up',
            })
        return {'type': 'ir.actions.act_window_close'}
