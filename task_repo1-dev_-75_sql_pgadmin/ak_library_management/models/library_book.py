# - * - coding: utf - 8 -*-
from odoo import models, fields
import logging
import psycopg2

_logger = logging.getLogger(__name__)
class Book(models.Model):

    _name = 'library.book'
    _description = 'Library Book'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    date_release = fields.Date(string='Publication Date')
    pages = fields.Integer(string='Pages')
    member_id = fields.Many2one(comodel_name='library.members',
                                 string='Members')
    author_id = fields.Many2one(comodel_name='library.author', string='Authors')
    category_ids = fields.Many2many(comodel_name='library.book.category',
                                    string='Category')
    library_id = fields.Many2one(comodel_name='library.library', string='Library')
    isbn_number = fields.Char(string='ISBN')
    book_state = fields.Selection([('borrowed', 'Borrowed'),('available', 'Available')],
                                  string='Book Status')

    # db connection
    conn = psycopg2.connect(dbname="library_db",
                            user="odoo",
                            password="library123")
    cur = conn.cursor()
    cur.execute("SELECT name FROM library_library")
    cur.execute("ALTER TABLE library_book ALTER COLUMN name SET NOT NULL")
    cur.execute("ALTER TABLE library_book ADD CONSTRAINT unique_isbn UNIQUE (isbn_number)")
    cur.execute("ALTER TABLE library_book ADD CONSTRAINT pages_capacity CHECK (pages > 0)")
    rows = cur.fetchall()
    for row in rows:
        print("Library name:",row)
    cur.close()
    conn.close()

    # SQL query use
    def fetch_first_five_books_names(self):
        """
          define: fetch_first_five_books_names
          description: function uses sql query to fetch 1st five book records.
          returns: None
        """
        query = """
        SELECT id, name 
        FROM library_book 
        ORDER BY id ASC 
        LIMIT 5;
        """
        self.env.cr.execute(query)
        result = self.env.cr.dictfetchall()
        for row in result:
            # print("Data------>", row['name'])
            _logger.info("Book: %s", row['name'])

    # ORM method use
    def fetch_books_pages_more_than_300_using_orm(self):
        """
          define: fetch_books_pages_more_than_300_using_orm
          description: function uses ORM method to search display the books names who's
                       pages are greater than 300.
          params: data
          returns: data
        """
        data = self.search([('pages','>', 300)])
        if data:
            print("The books count with pages more than 300:", len(data))
            for book in data:
                print("Book Name: ", book.name)
        else:
            print("No books found")
        return data
