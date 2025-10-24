# - * - coding: utf - 8 -*-
from odoo import models, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('product_id')
    def _check_book_borrowed(self):
        """
        define: _check_book_borrowed
        description: check and validates for the borrowed book to not be added
                     in sale order.
        params: product_id
        returns: none
        """
        for line in self:
            product = line.product_id
            if product.is_library_book:
                if product.status == 'borrowed':
                    raise ValidationError(f"The book '{product.name}' is already "
                                          f"borrowed and cannot be added to this "
                                          f"sale order.")
