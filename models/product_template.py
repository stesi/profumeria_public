from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(related='x_producer', store=True)