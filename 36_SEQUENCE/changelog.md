# Library Management System
 
### Technical Name: ak_library_management
 
## [18.0.1.0.0] - 2025-09-01 | Dynamic sequenceing
- The scope of Work for the task: ir.sequence​:
In the library_management module, we will add two new fields in the Book and Members model, which will auto-generate a sequence :

- Fields Definition:
- Model: product.template​
- ​reference (Char): Utilise existing Reference​ field to create a unique sequence for that record.
- Model: library.member
- ​membership_no (Char)​:  Define/utilize Member ID​ field to create a unique sequence for that record.

IR Sequence Implementation:
- Create an ir.sequence​ for generating a unique Book Reference (reference​) with a format like BOOK-2025-0001.
- Create an ir.sequence​ for generating a unique Membership ID (membership_id​) with a format like MEM-2025-02-0001.
- Assign these sequences using the model’s create method to ensure automatic number generation.
