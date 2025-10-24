from odoo import models, fields

class Student(models.Model):
    _name = 'student.student'
    _description = 'Student Record'

    name = fields.Char(string="Name")
    description = fields.Text(string="Description")