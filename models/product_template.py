from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(compute="_compute_brand", store=True)

    @api.depends("product_brand_ept_id")
    def _compute_brand(self):
        for product in self:
            product.brand = str(product.product_brand_ept_id.name)

    @api.model
    def fields_get(self, fields=None, attributes=None):
        fields_to_hide = ['brand']
        res = super(ProductTemplate, self).fields_get(fields,attributes)
        for field in fields_to_hide:
            if field in res:
                res[field]['searchable'] = False
                res[field]['sortable'] = False
        return res
