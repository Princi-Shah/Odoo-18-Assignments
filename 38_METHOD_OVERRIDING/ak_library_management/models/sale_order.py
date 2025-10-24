# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_flag = fields.Boolean(string='Approval Needed', default=True)
    approval_done = fields.Boolean(string='Approval Done', default=False)
    is_approval_manage = fields.Boolean(string='Button Needed', default=False)
    is_sales_manager = fields.Boolean(compute='_compute_is_sales_manager',store=False)

    def _compute_is_sales_manager(self):
        """
        define: _compute_is_sales_manager
        description: function to manage sale manager
        returns: None
        """
        for rec in self:
            rec.is_sales_manager = self.env.user.is_manager

    def action_confirm(self):
        """
        define: action_confirm
        description: manage the base and custom confirm button working visibility
                     and also triggering warning when action performed.
        returns: base confirm method
        """
        low_stock_books = [
            line.product_id.name
            for line in self.order_line
            if line.product_id.qty_available < 5
        ]

        if low_stock_books and not self.is_approval_manage:
            self.approval_flag = False
            self.approval_done = True
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'warning',
                    'sticky': False,
                    'message': _("Approval needed! The following books have low"
                                 " stock:\n %s", ', '.join(low_stock_books)),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        elif low_stock_books and self.approval_done:
            self.approval_flag = True
            self.approval_done = False
            return super().action_confirm()
        else:
            self.approval_flag = True
            self.approval_done = True
            return super().action_confirm()

    def action_approve(self):
        """
        define: action_approve
        description: function to manage Approve button
                     visibility according to the user
        returns: None
        """
        self.is_approval_manage = True
        if not self.is_sales_manager:
            self.is_sales_manager = False
        else:
            self.approval_flag = True
            self.approval_done = False

    def action_reject(self):
        """
        define: action_reject
        description: function to manage Reject button
                     visibility according to the user
        returns: None
        """
        if not self.is_sales_manager:
            self.is_sales_manager = False
        else:
            self.approval_flag = True
            self.action_cancel()
