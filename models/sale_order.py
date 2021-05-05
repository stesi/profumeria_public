import re

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tax_vat_number = fields.Char()
    pec_sdi_code = fields.Char()

    def set_payment_terms_from_pay_method(self, transaction):
        if not transaction:
            transaction = self.get_portal_last_transaction()
        if transaction:
            term_id = transaction.acquirer_id.payment_term_id
            if term_id:
                self.payment_term_id = term_id
            else:
                pass

    def remove_tax_from_delivery(self):
        product_delivery = []
        for delivery in self.env['delivery.carrier'].search([]):
            product_delivery += delivery.product_id
        if len(product_delivery) > 0:
            for line_delivery in self.order_line.filtered(lambda l: l.product_id in product_delivery):
                line_delivery.update({'tax_id': False})
