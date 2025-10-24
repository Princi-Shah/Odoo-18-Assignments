# Library Management System
 
### Technical Name: ak_library_management
 
## [18.0.1.0.0] - 2025-10-24 | Book Reservation System
- Reservation Model
Fields:
customer_id → Many2one('res.partner') (Customer)
book_id → Many2one('product.template') (Book)
reservation_date → Datetime (Default = Today)
expected_pickup_date → Datetime (Required)
state → Selection
Draft
Reserved
Cancelled
Picked Up

- Extend Customer (res.partner)
Add field can_reserve_books → Boolean
Indicates if customer can make reservations.

- Reservation Views
- List View
Show: Customer, Book, Reservation Date, Expected Pickup Date, State.
- Form View
Allow editing reservation and changing state.
- Search View
Group by: Customer, Book, State.

- Menu
Menu Location: Sales → Products → Reservations
Opens list view of reservations.

- Reservation Wizard
Button on product.template: Reserve Book
- Wizard Fields:
customer_id → Many2one('res.partner', required, domain=[('can_reserve_books', '=', True)])
book_id → Many2one('product.template', readonly, pre-filled)
expected_pickup_date → Datetime (Required)
- Wizard Buttons:
Cancel → Close wizard.
Confirm → Create new record in book.reservation with:
state = "Reserved".

- Smart Buttons
Customer Form View (res.partner)
Smart button: Reservations
Shows count of reservations for that customer.
On click → open book.reservation tree view filtered by customer.
Book Form View (product.template)
Smart button: Reservations
Shows count of reservations for that book.
On click → open book.reservation tree view filtered by book.

- Advanced ORM & Display Logic Task
1. Custom name_search on Reservation
​add method  in book.reservation
- Allow searching reservations by:
Customer Name
Book Name
Reservation Date (string format)
2. Custom _compute_display_name
​In book.reservation, search record with format as 
[Customer] - [Book] (Expected Pickup: Date)
3. Using read & search_read
Add a menu action that calls a custom server action method action_export_reservations.
Inside that method:
- Use read() to fetch fields of reservations (customer_id, book_id, state).
- Use search_read() to fetch reservations in state "Reserved".

- Used read and search_read method for export_reservations data
- Removed default False on boolean fields.
- Removed display name (Please research on compute display name)
- Improved Xpath of the action_view_reservations button
- Removed unnecessary depend module in Manifest file 

