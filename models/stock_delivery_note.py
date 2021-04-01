from odoo import api, fields, models


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    payment_term_ids = fields.One2many('account.payment.term', compute="_compute_payment_term_ids")

    @api.depends("sale_ids")
    def _compute_payment_term_ids(self):
        for ddt in self:
            ddt.payment_term_ids = ddt.sale_ids.mapped("payment_term_id")
