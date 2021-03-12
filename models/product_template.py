from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(compute="_compute_brand")

    @api.depends("product_brand_ept_id")
    def _compute_brand(self):
        for product in self:
            product.brand = str(product.product_brand_ept_id.name)

