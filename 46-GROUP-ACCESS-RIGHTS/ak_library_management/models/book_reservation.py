# - * - coding: utf - 8 -*-
from odoo import fields, models, api,_
from odoo.exceptions import UserError
from odoo.tools import format_date

class BookReservation(models.Model):
    _name = 'book.reservation'
    _description = 'Book Reservation'

    customer_id = fields.Many2one('res.partner',
                                  string='Customer',
                                  required=True)
    book_id = fields.Many2one('product.template', string='Book')
    reservation_date = fields.Datetime(string='Reservation Date',
                                       default=fields.Datetime.now)
    expected_pickup_date = fields.Datetime(string='Expected Pickup Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('cancelled', 'Cancelled'),
        ('picked up', 'Picked Up'),
    ], string='Status', default='draft')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name',
                               store=True)

    def action_reservation_button(self):
        """
        define: action_reservation_button
        description: function helps perform the state change to reserve when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.check_borrowing_limit()
            record.state = 'reserved'

    def action_cancel_button(self):
        """
        define: action_cancel_button
        description: function helps perform the state change to cancelled when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.state = 'cancelled'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        define: name_search
        description: function helps perform the name_search and add the filter for
                    customer name, book name and reservation date.
        returns: None
        """
        args = args or []
        domain = []
        if name:
            domain = [
                '|', '|',
                ('customer_id.name',operator, name),
                ('book_id.name',operator, name),
                ('reservation_date',operator, name),
            ]
        return self._search(domain + args, limit=limit)

    @api.depends('customer_id.name', 'book_id.name', 'expected_pickup_date')
    def _compute_display_name(self):
        """
        define: _compute_display_name
        description: function helps perform the pass of the values of
                    customer name, book name and expected pick up date to be visible
                    when book is reserved
        returns: customer_id, book_id, expected_pickup_date
        """
        for record in self:
            date_str = format_date(self.env, record.expected_pickup_date,
                                   date_format='yyyy-MM-dd')
            record.display_name = (
                f"[{record.customer_id.name}] - [{record.book_id.name}] "
                f"(Expected Pickup: {date_str})")

    @api.model
    def action_export_reservations(self):
        """
        define: action_export_reservations
        description: function helps pass the data of exported data
        returns: None
        """
        domain = [('state', '=', 'reserved')]
        reserved_dataset = self.env['book.reservation'].search(domain)
        for records in reserved_dataset:
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 'simple_notification',
                {
                    'title': 'Export Data',
                    'message': f'Reserved data: {records.customer_id.name} '
                                   f'Reserved : {records.book_id.name} '
                                   f'with state: {records.state}',
                    'sticky': True,
                })
        return {'type': 'ir.actions.client'}
    
    def check_borrowing_limit(self):
        """
        define: check_borrowing_limit
        description: function helps monitor the number of reservations made by
                     particular user
        returns: user error
        """
        limit = int(self.env['ir.config_parameter'].sudo().get_param(
            'ak_library_management.library_borrowing_limit', default=0
        ))
        current_borrowed = self.env['book.reservation'].search_count([
            ('customer_id', '=', self.customer_id.id),
            ('state', 'in', ['reserved', 'picked_up'])
        ])
        if current_borrowed >= limit:
            raise UserError(
                f"Borrowing limit reached! This member already has {current_borrowed} "
                f"book(s) and cannot borrow more than {limit}."
            )
        

    def action_open_pick_up_wizard(self):
        """
        define: action_open_pick_up_wizard
        description: function helps view the filled user data inside the wizard by
                     fatching it from the  source
        returns: wizard
        """
        self.ensure_one()
        return {
            'name': 'Confirm Book Pick Up',
            'type': 'ir.actions.act_window',
            'res_model': 'reserve.book.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('ak_library_management.reserve_book_wizard_form').id,
            'context': {
                'default_reservation_id': self.id,
                'default_customer_id': self.customer_id.id,
                'default_book_id': self.book_id.id,
            },
            'target': 'new',
        }

    @api.model
    def create(self, vals):
        """
        define: create
        description: function helps create a new record every time the action is called.
        returns: create method of book reservation
        """
        user = self.env.user
        target_state = vals.get('state', 'draft')

        if (user.has_group('ak_library_management.group_library_assistant') and
        not user.has_group('ak_library_management.group_library_admin')):
            if target_state not in ['reserved', 'draft']: 
                raise UserError(_("Library Assistants can only create new reservations "
                                  "in the 'Reserved' state."))
            elif target_state == 'reserved':
                vals['state'] = 'reserved'
        if (user.has_group('ak_library_management.group_library_worker') and
        not user.has_group('ak_library_management.group_library_assistant')):
            raise UserError(_("Library Workers are not allowed to create book "
                              "reservation records."))
        return super(BookReservation, self).create(vals)
