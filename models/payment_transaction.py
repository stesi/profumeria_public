from odoo import fields, models, api


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def set_sales_payment_terms_from_pay_method(self):
        for sale in self.sale_order_ids:
            sale.set_payment_terms_from_pay_method(self)
