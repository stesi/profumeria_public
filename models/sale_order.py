import re

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def remove_tax_from_delivery(self):
        product_delivery = []
        for delivery in self.env['delivery.carrier'].search([]):
            product_delivery += delivery.product_id
        if len(product_delivery) > 0:
            for line_delivery in self.order_line.filtered(lambda l: l.product_id in product_delivery):
                line_delivery.update({'tax_id': False})