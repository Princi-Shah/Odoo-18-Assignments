# - * - coding: utf - 8 -*-
from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    can_reserve_books = fields.Boolean(string='Can Reserve Books',
                                       default=False)
    reservation_count = fields.Integer(compute='_compute_reservation_count')

    def _compute_reservation_count(self):
        """
        define: _compute_reservation_count
        description: function helps calculate the reservation count by customers
        returns: None
        """
        for partner in self:
            partner.reservation_count = self.env['book.reservation'].search_count(
                [('customer_id', '=', partner.id)])

    def action_view_reservations(self):
        """
        define: action_view_reservations
        description: function helps view the reservation data in list and form view.
        returns: None
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Reservations',
            'view_mode': 'list,form',
            'res_model': 'book.reservation',
            'domain': [('customer_id', '=', self.id)],
        }

    def send_mail(self):
        """
        define: send_mail
        description: function helps perform the send mail functionality.
        returns: None
        """
        mail_template = self.env.ref('mail.mail_template_test').with_context(
            lang=self.env.user.lang)
        mail_template.sudo().send_mail(self.id, force_send=True)
