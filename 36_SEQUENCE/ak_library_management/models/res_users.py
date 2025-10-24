from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'
    is_manager=fields.Boolean(string="Is Manager")
