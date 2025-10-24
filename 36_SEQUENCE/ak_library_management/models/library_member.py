# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Members'

    name = fields.Char(string='Member Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    membership_date = fields.Date(string='Membership Start Date', required=True)
    membership_no = fields.Char(string="Membership ID", readonly=True, copy=False,
                                index=True)

    @api.model
    def create(self, vals):
        """
        define: create
        description: it generates the dynamic sequence as member is created
        params: vals
        returns: library_member
        """
        if not vals.get("membership_no"):
            vals["membership_no"] = (
                self.env["ir.sequence"].next_by_code("library.member") or _("New")
            )
        return super(LibraryMember, self).create(vals)
