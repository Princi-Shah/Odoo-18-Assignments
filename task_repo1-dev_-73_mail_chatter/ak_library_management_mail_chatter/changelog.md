# Library Management System
 
### Technical Name: ak_library_management_mail_chatter
 
## [18.0.1.2.0] - 2025-08-19 | Odoo buttons and smart buttons
- Task 1:
- Add Chatter functionality on the Libariry model and add tracking on the fields.
- Update chatter message on the book.
- When a book is borrowed, log a message in the chatter of the book record.
- The message should contain the borrower's name and the date of borrowing.
- Add a custom log note in the chatter whenever a book is returned.
- Add chatter on the library model.

- Task 2:
- Whenever a book is borrowed, create an activity assigned to the current login user to remind them of the book's due date.
- Default activity To-Do
- Deadline 10 Days from the borrowed date
- The activity should contain the borrower's details and the due date for returning the book.
- Use the activity_schedule method to create the activity.

- Task 3:
- Send a notification to the current user when a book status is updated in the current library.
- Implement a functionality while creating a bulk product to notify the current user with the created book name one by one with on-display notification.
- Use self.env['bus.bus']._sendone to show a notification when the bulk update is successful.
Note:If the 'librarian' field does not exist in the Library model, add a Many2one field referencing 'res.users' as 'librarian_id' and send a notification to the assigned librarian.
