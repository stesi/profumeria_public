from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand = fields.Char(related='product_tmpl_id.brand', store=True)