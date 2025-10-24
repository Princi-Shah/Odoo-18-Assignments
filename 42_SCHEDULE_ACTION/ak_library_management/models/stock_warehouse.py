# - * - coding: utf - 8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    library_assistant_id = fields.Many2one('hr.employee', string='Library Assistant')
    worker_ids = fields.Many2many('hr.employee', string='Library Workers')

    _sql_constraints = [
        ('unique_assistant', 'unique(library_assistant_id)',
         'This employee is already assigned as a Library Assistant to another '
         'warehouse!'),
    ]

    @api.constrains('worker_ids')
    def _check_unique_worker(self):
        """
        define: _check_unique_worker
        description: function helps constrain the specified user worker
        returns: validation error
        """
        for rec in self:
            for worker in rec.worker_ids:
                other = self.search([
                    ('id', '!=', rec.id),
                    ('worker_ids', 'in', [worker.id])
                ], limit=1)
                if other:
                    raise ValidationError(
                        f"Employee {worker.name} is already assigned as a worker in "
                        f"another warehouse!"
                    )
