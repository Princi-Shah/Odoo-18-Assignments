# - * - coding: utf - 8 -*-
from odoo import fields, models

class ReserveBookWizard(models.TransientModel):
    _name = 'reserve.book.wizard'
    _description = 'Reserve Book Wizard'

    customer_id = fields.Many2one('res.partner',
                                  string='Customer',
                                  required=True,
                                  domain=[('can_reserve_books', '=', True)], 
                                  readonly=True)
    book_id = fields.Many2one('product.template',
                              string='Book',
                              readonly=True)
    reservation_id = fields.Many2one('book.reservation', string="Reservation",
                                     required=True)

    def action_pick_up(self):
        """
        define: action_pick_up
        description: function helps perform the picked up method on call of pick up
                     button inside wizard.
        returns: window action
        """
        self.env['book.reservation'].create({
            'customer_id': self.customer_id.id,
            'book_id': self.book_id.id,
            'state': 'picked up',
        })
        return {'type': 'ir.actions.act_window_close'}
