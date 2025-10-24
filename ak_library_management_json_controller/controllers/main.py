# - * - coding: utf - 8 -*-

from odoo import http
from odoo.http import request


class CustomerFetchDataController(http.Controller):
    @http.route('/customers', type="http", auth="public", website=True)
    def customer_page(self, **kwargs):
        return request.render('ak_library_management.customer_detail_template')

    @http.route('/action_send_mail', type="json", auth="public", website=True)
    def action_send_mail(self, **kwargs):
        customerdetails=[]
        customers = request.env['library.members'].sudo().search([('email', '=', kwargs.get('values'))])
        for customer in customers:
            customerdetails.append({
                    'customer_name': customer.name,
                    'customer_phone': customer.phone
                })
            # if not customer:
            #     print("in if")
            #     return {'error': 'No such customer'}
            # else:
            #     print("inelse")
            #     return {
            #         'customer_name': customer.name,
            #         'customer_phone': customer.phone
            #     }
        print("===", customerdetails)
        return customerdetails





        # customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
        # if not customer:
        #     return {'error': 'No such customer'}
        # else:
        #     return {'customer name': customer.name,
        #             'customer email': customer.email,
        #             'customer id': customer.id,
        #             }
