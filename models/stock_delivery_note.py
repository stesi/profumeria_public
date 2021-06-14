from lxml import etree

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import json


class StockDeliveryNote(models.Model):
    _inherit = 'stock.delivery.note'

    payment_term_ids = fields.One2many('account.payment.term', compute="_compute_payment_term_ids")

    margin = fields.Float(compute="_compute_margin", store=True)
    force_add_manually_line = fields.Boolean(related="type_id.force_add_manually_line")

    @api.onchange("line_ids")
    def check_line_ids(self):
        if self.line_ids.filtered(lambda l: not l.create_date):
            if not self.force_add_manually_line:
                raise ValidationError("Not allowed to create manually line")

    @api.depends("sale_ids")
    def _compute_margin(self):
        for ddt in self:
            ddt.margin = 0
            for sale in ddt.sale_ids:
                ddt.margin += sale.margin

            if ddt.type_id.compute_negative_price and ddt.margin > 0:
                ddt.margin = ddt.margin * -1

    countersign = fields.Boolean(string="Countersign", compute='compute_countersign')

    def compute_countersign(self):
        for delivery in self:
            wc_payment_gateway_id = delivery.sale_ids.mapped("wc_payment_gateway_id").filtered(
                lambda l: l.countersign == True)
            if len(wc_payment_gateway_id) > 0:
                delivery.countersign = True
            else:
                delivery.countersign = False

            if delivery.countersign == False:
                if len(delivery.payment_term_ids.filtered(lambda l: l.countersign == True)) > 0:
                    delivery.countersign = True
                else:
                    delivery.countersign = False

    total_prices = fields.Float(compute="_compute_total_prices", store=True)

    currency_id = fields.Many2one('res.currency', related="partner_id.currency_id")

    @api.depends("line_ids")
    def _compute_total_prices(self):
        for ddt in self:
            if len(ddt.line_ids) > 0:
                ddt.total_prices = float(sum(l.price_unit * l.product_qty for l in ddt.line_ids))
            else:
                ddt.total_prices = 0

            if ddt.type_id.compute_negative_price and ddt.total_prices > 0:
                ddt.total_prices = ddt.total_prices * -1

    @api.depends("sale_ids")
    def _compute_payment_term_ids(self):
        for ddt in self:
            ddt.payment_term_ids = ddt.sale_ids.mapped("payment_term_id")
