from odoo import api, fields, models


class StockDeliveryNoteType(models.Model):
    _inherit = 'stock.delivery.note.type'

    compute_negative_price = fields.Boolean(default=False)
    force_add_manually_line = fields.Boolean()
