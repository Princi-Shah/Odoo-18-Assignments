# - * - coding: utf - 8 -*-
from odoo import fields, models, api
from odoo.tools import format_date

class BookReservation(models.Model):
    _name = 'book.reservation'
    _description = 'Book Reservation'

    customer_id = fields.Many2one('res.partner',
                                  string='Customer',
                                  required=True,
                                  domain=[('can_reserve_books', '=', True)])
    book_id = fields.Many2one('product.template', string='Book')
    reservation_date = fields.Datetime(string='Reservation Date',
                                       default=fields.Datetime.now)
    expected_pickup_date = fields.Datetime(string='Expected Pickup Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('cancelled', 'Cancelled'),
        ('picked up', 'Picked Up'),
    ], string='Status', default='draft')

    def action_reservation_button(self):
        """
        define: action_reservation_button
        description: function helps perform the state change to reserve when button
                    is clicked.
        returns: None
        """
        for record in self:
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

    def action_picked_up_button(self):
        """
        define: action_picked_up_button
        description: function helps perform the state change to picked up when button
                    is clicked.
        returns: None
        """
        for record in self:
            record.state = 'picked up'

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
            date_str = ''
            if record.expected_pickup_date:
                date_str = format_date(self.env, record.expected_pickup_date, date_format='yyyy-MM-dd')

            record.display_name = (
                f"[{record.customer_id.name or 'Unknown'}] - "
                f"[{record.book_id.name or 'No Book'}] "
                f"(Expected Pickup: {date_str})"
            )

    @api.model
    def action_export_reservations(self):
        """
        define: action_export_reservations
        description: function helps pass the data of exported data
        returns: None
        """
        domain = [('state', '=', 'reserved')]
        reserved_dataset = self.env['book.reservation'].search_read(domain, ['customer_id', 'book_id', 'state'])
        for records in reserved_dataset:
            customer_name = records['customer_id'][1] if records['customer_id'] else 'Unknown'
            book_name = records['book_id'][1] if records['book_id'] else 'Unknown'
            state = records.get('state', 'N/A')
            self.env['bus.bus']._sendone(
                self.env.user.partner_id, 'simple_notification',
                {
                    'title': 'Export Data',
                    'message': f'Reserved data: {customer_name} '
                                   f'Reserved : {book_name} '
                                   f'with state: {state}',
                    'sticky': True,
                })
        return {'type': 'ir.actions.client'}
