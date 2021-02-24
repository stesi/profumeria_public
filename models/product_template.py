from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(store=True)

    @api.model
    def fields_get(self, fields=None):
        fields_to_hide = ['product_brand_ept_id']
        res = super(ProductTemplate, self).fields_get()
        for field in fields_to_hide:
            res[field]['searchable'] = False
        return res
