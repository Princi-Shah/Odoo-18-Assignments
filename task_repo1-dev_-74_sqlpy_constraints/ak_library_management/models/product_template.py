# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_library_book = fields.Boolean(string='Is Library Book')
    library_id = fields.Many2one('library.library', string='Library')
    status = fields.Selection(
        selection=[('available', 'Available'),
                   ('borrowed', 'Borrowed')],
        string='Book Status',
        default='available'
    )

    @api.constrains('is_library_book', 'library_id')
    def _check_library_book(self):
        """
        define: _check_library_book
        description: checks if the product added in the library is a library product or
                     not with that it also checks and validates for the library books
                     to only be added by library managers and also checks if books count
                     exceeds the capacity count of the library.
        params: is_library_book, library_id
        returns: none
        """
        not_library_books = self.filtered(lambda b: not b.is_library_book and b.library_id)
        if not_library_books:
            names = "\n".join(not_library_books.mapped("name"))
            raise ValidationError(
                f"The following products cannot be added to '{self.library_id.name}' "
                f"because they are not library books: \n{names}"
            )

        for book in self:
            if book.is_library_book and book.library_id:
                if not self.env.user.is_library_manager:
                    raise ValidationError(
                        "You are not allowed to add books!!"
                        "Only library managers can add books to library."
                    )

                current_count = len(book.library_id.book_ids)
                if current_count > book.library_id.capacity:
                    raise ValidationError(
                        f"Cannot add '{book.name}' to '{book.library_id.name}' "
                        f"because it has reached its capacity of "
                        f"{book.library_id.capacity} books."
                    )

    def action_mark_borrowed(self):
        """
        define: action_mark_borrowed
        description: change the book status to 'Borrowed' when clicked on borrowed button.
        params: none
        returns: none
        """
        for record in self:
            record.status = 'borrowed'

    def action_mark_available(self):
        """
        define: action_mark_available
        description: change the book status to 'Available' when clicked on available button.
        params: none
        returns: none
        """
        for record in self:
            record.status = 'available'

    def action_return_book(self):
        """
        define: action_return_book
        description: change the book status to 'Available' when clicked on return button.
        params: none
        returns: none
        """
        for record in self:
            record.status = 'available'
            