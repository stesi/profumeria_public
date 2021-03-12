from odoo import api, fields, models


class StockDeliveryNoteLine(models.Model):
    _inherit = 'stock.delivery.note.line'

    product_barcode = fields.Char(related="product_id.barcode", string="Barcode")