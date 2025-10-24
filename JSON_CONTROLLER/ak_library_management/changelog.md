# Library Management System
 
### Technical Name: ak_library_management
 
## [18.0.1.2.0] - 2025-08-19 | Odoo buttons and smart buttons
- Add a Status Button in the Book Model 
- Modify the Book model (product.template) to include a status field and a button to change the status.
The status should have the following values:
Available
Borrowed
Reserved
- Steps:
Add a status field (fields.Selection) to track the book's status.
Create a button Mark as Borrowed that sets the status to Borrowed.
Create a button Mark as Available that sets the status back to Available.
Display the button conditionally based on the current status (i.e., show Mark as Borrowed only when the book is Available).
- Task 2: Add a Smart Button to Show Borrowed Books in the Library Model
Modify the Library model (library.library) to include a smart button that displays the number of books borrowed.

- Steps:
Create a compute function to count the number of books borrowed from the current library.
Add a smart button with proper icons for the smart button in the library form to show the count of borrowed books used.
When the user clicks the smart button, it should open a list view showing all borrowed books from the current library.

- Bonus Task (Optional): Implement a Return Feature:

- Add a button Return Book to allow a member to return a book.
Once returned, update the book's status to Available.
