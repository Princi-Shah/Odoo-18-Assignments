# Library Management System
 
### Technical Name: ak_library_management
 
## [18.0.1.0.0] - 2025-10-14 | Schedule Actions, Server Action and Mail sending
- A scheduled action that runs daily and checks for borrowing transactions where the return date is approaching. It will send a reminder to customers to return their reserved books.
- This server action allows users to manually mark books as returned when customers return them.
- Automatically prevents customers from reserving new books if they have overdue books. Apply below logic while creating and updating the record.
