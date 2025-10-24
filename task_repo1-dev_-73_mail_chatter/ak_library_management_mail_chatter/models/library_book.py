# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta

class Book(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, tracking=True)
    date_release = fields.Date(string='Publication Date')
    book_state = fields.Selection([('available', 'Available'),
                                   ('borrowed', 'Borrowed'), ],
                                  string='book_state',
                                  default='available',
                                  tracking=True)
    borrow_date = fields.Date(string='Borrow Date', tracking=True)
    due_date = fields.Date(string='Due Date', compute='_compute_due_date', store=True,
                           readonly=True)
    library_id = fields.Many2one(comodel_name='library.library', string='Library',
                                 tracking=True)
    borrower_member_id = fields.Many2one(comodel_name='library.members',
                                         string='Borrower member',tracking=True)
    author_ids = fields.Many2many(comodel_name='library.author',
                                  string='Authors')
    category_id = fields.Many2one(comodel_name='library.book.category',
                                  string='Category')
    library_location = fields.Char(string='Library Location',
                                   related='library_id.location', store=True)
    book_reference = fields.Char(string='Book Reference',
                                 compute='_compute_book_reference', store=True)

    @api.depends('borrow_date')
    def _compute_due_date(self):
        """
        define: _compute_due_date
        description: function helps calculate the number of days after teh book borrow date
        params: borrow_date
        returns: None
        """
        for record in self:
            record.due_date = record.borrow_date + timedelta(days=10) if record.borrow_date else False

    @api.depends('name', 'author_ids')
    def _compute_book_reference(self):
        """
        define: _compute_book_reference
        description: function helps auto-fill the reference field data with name and author_ids
        params: name, author_ids
        returns: None
        """
        for record in self:
            if record.name and record.author_ids:
                authors = ', '.join(record.author_ids.mapped('name'))
                record.book_reference = f"{record.name} - {authors}"
            else:
                record.book_reference = ''

    @api.onchange('book_state')
    def _onchange_book_state(self):
        """
        define: _onchange_book_state
        description: function helps auto change the state when book is borrowed or returned
        params: book_state
        returns: None
        """
        if self.book_state == 'available':
            self.borrower_member_id = False
            self.borrow_date = False

    def action_mark_borrowed(self):
        """
        define: action_mark_borrowed
        description: function helps perform the action when book is borrowed and also
                     helps send the notification update
        returns: None
        """
        for record in self:
            record.book_state = 'borrowed'
            record.borrow_date = date.today()

            # Log a message in the book model chatter when it is borrowed
            if record.borrower_member_id:
                record.message_post(
                    body=f"Book borrowed by {record.borrower_member_id.name} on {record.borrow_date}"
                )

            # Create a To-Do activity for the current user
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=self.env.user.id,
                summary=f'Return book: {self.name}',
                note=f'Reminder to return book "{self.name}" borrowed by '
                f'{self.borrower_member_id.name}. Due date is {self.due_date}.',
                date_deadline=self.due_date
            )

            # Notifyy current user
            record.env['bus.bus']._sendone(
                record.env.user.partner_id,
                'simple_notification',
                {
                    'title': 'Book Borrowed',
                    'message': f'Book {record.name} borrowed '
                               f'by {record.borrower_member_id.name}'
                }
            )

    def action_mark_available(self):
        """
        define: action_mark_available
        description: function helps perform the action when book is available and also
                     helps send the notification update
        returns: None
        """
        for record in self:
            record.book_state = 'available'

    def action_return_book(self):
        """
        define: action_return_book
        description: function helps perform the action when book is returned and also
                     helps send the notification update
        returns: None
        """
        self.ensure_one()
        if self.book_state == 'borrowed':
            borrower_name = self.borrower_member_id.name

            # Add custom log note when book is return
            self.message_post(
                body=f"Book returned by {borrower_name} on {fields.Date.today()}"
            )

            self.borrower_member_id = False
            self.borrow_date = False
            self.book_state = 'available'

            # Notify current user
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                'simple_notification',
                {
                    'title': 'Book Returned',
                    'message': f'Book {self.name} returned '
                               f'by {self.borrower_member_id.name}'
                }
            )
            # Notify librarian if book operation performed
            if self.library_id.librarian_id:
                self.message_post(
                    body=f'Book {self.name} returned '
                         f'by {self.borrower_member_id.name}',
                    partner_ids=[self.library_id.librarian_id.partner_id.id]
                )

    def action_create_bulk_books(self, book_names):
        """
        define: action_create_bulk_books
        description: function helps perform the action helps send the notification
                     update to the librarian and current user the books name notification.
        params: book_names
        returns: book
        """
        library_id = self.env.context.get('default_library_id', False)
        for name in book_names:
            book = self.create({
                'name': name,
                'library_id': library_id if library_id else False
                })
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                'simple_notification',
                {
                    'title': 'Book Created',
                    'message': f'Book {name} created successfully'
                }
            )

            # Notify librarian if assigned
            if book.library_id.librarian_id:
                book.message_post(
                    body=f'Book {book.name} created',
                    partner_ids=[book.library_id.librarian_id.partner_id.id]
                )
        return book

    #craeting the activity_schedule method when craeting the activity
    def write(self, vals):
        old_state = {rec.id: rec.book_state for rec in self}
        res = super(Book, self).write(vals)
        if 'book_state' in vals:
            self.env['bus.bus']._sendone(
                self.env.user.partner_id,
                "simple_notification",
                {
                    "title": "Book Status Updated",
                    "message": f"Status of {self.name} changed to {vals["book_state"]}",
                    "sticky": True
                }
            )
            # Sending a notification to the current user when a book status is updated from the library.
            for record in self:
                if record.book_state != old_state.get(record.id):
                    message_body = (f"Status of the book '{record.name}' has been updated "
                                    f"from '{old_state.get(record.id)}' "
                                    f"to '{record.book_state}'")
                    record.message_post(
                        body=message_body,
                        partner_ids=[self.env.user.partner_id.id]
                    )
                # Notify librarian when state chnages
                if self.library_id.librarian_id:
                    self.message_post(
                        body=f"Book {self.name} status changed to {vals["book_state"]}",
                        partner_ids=[self.library_id.librarian_id.partner_id.id]
                    )
        return res
