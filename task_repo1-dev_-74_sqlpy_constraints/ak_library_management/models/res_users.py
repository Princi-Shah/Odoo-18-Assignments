# -*- coding: utf-8 -*-
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_library_manager = fields.Boolean(string = "Is library Manager")
