# - * - coding: utf - 8 -*-
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    library_borrowing_limit = fields.Integer(
        string="Max Books to Borrow",
        config_parameter='ak_library_management.library_borrowing_limit',
        default=0,
    )
    