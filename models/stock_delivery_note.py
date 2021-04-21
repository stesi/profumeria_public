from odoo import api, fields, models


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    payment_term_ids = fields.One2many('account.payment.term', compute="_compute_payment_term_ids")

    countersign = fields.Boolean(string="Countersign", compute='compute_countersign')

    def compute_countersign(self):
        for delivery in self:
            payment_term_ids = delivery.sale_ids.mapped("wc_payment_gateway_id").filtered(lambda l: l.countersign == True)
            if len(payment_term_ids) > 0:
                delivery.countersign = True
            else:
                delivery.countersign = False

    @api.depends("sale_ids")
    def _compute_payment_term_ids(self):
        for ddt in self:
            ddt.payment_term_ids = ddt.sale_ids.mapped("payment_term_id")
