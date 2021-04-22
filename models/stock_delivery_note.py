from odoo import api, fields, models


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    payment_term_ids = fields.One2many('account.payment.term', compute="_compute_payment_term_ids")

    countersign = fields.Boolean(string="Countersign", compute='compute_countersign')

    total_prices = fields.Float(compute="_compute_total_prices", store=True)

    currency_id = fields.Many2one('res.currency', related="partner_id.currency_id")

    @api.depends("line_ids")
    def _compute_total_prices(self):
        for ddt in self:
            if len(ddt.line_ids) > 0:
                ddt.total_prices = float(sum(l.price_unit * l.product_qty for l in ddt.line_ids))
            else:
                ddt.total_prices = 0

    def compute_countersign(self):
        for delivery in self:
            payment_term_ids = delivery.sale_ids.mapped("payment_term_id").filtered(lambda l: l.countersign == True)
            if len(payment_term_ids) > 0:
                delivery.countersign = True
            else:
                delivery.countersign = False

    @api.depends("sale_ids")
    def _compute_payment_term_ids(self):
        for ddt in self:
            ddt.payment_term_ids = ddt.sale_ids.mapped("payment_term_id")
