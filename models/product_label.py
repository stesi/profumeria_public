from odoo import api, fields, models


class ProductLabel(models.Model):
    _inherit = 'product.label'

    activate_website_description = fields.Boolean()
    website_description = fields.Text()
