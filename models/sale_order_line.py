
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand = fields.Char(related='product_id.brand', store=True)