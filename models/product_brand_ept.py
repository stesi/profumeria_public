from odoo import api, fields, models


class ProductBrandEpt(models.Model):
    _inherit = 'product.brand.ept'

    activate_website_description = fields.Boolean()
    website_description = fields.Text()
