
from odoo import api, fields, models


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    brand = fields.Char(related='product_id.brand', store=True)