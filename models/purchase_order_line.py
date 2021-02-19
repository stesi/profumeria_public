
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    brand = fields.Char(related='product_id.brand', store=True)