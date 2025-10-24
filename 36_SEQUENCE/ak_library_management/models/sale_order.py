from odoo import api, fields, models
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('to_approve', 'To Approve'),
                                            ('rejected', 'Rejected'),])

    def action_confirm(self):
        for rec in self:
            low_stock_books = []
            for line in rec.order_line:
                if line.product_id.is_library_book and line.product_id.qty_available < 5:
                    low_stock_books.append(line.product_id.name)

            if low_stock_books:
                raise UserError(
                    f"The following library books have less than 5 in stock: {', '.join(low_stock_books)}"
                )
            rec.state = 'to_approve'
        return True

    def action_approve(self):
        if not self.env.user.is_manager:
            raise UserError("Only Managers can approve orders.")
        super(SaleOrder, self).action_confirm()
        return True

    def action_reject(self):
        if not self.env.user.is_manager:
            raise UserError("Only Managers can reject orders.")
        self.write({'state': 'rejected'})
        return True
