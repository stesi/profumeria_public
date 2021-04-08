from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(compute="_compute_brand", store=True)

    #minimum points
    minimum_point = fields.Float('Min Points', compute='_compute_min', store=True)

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

    @api.depends('product_variant_ids')
    def _compute_min(self):
        for rec in self:
            if len(rec.product_variant_ids) == 1:
                rec.minimum_point = rec.product_variant_ids.minimum_point
            else:
                h_min = rec.product_variant_ids[0].minimum_point
                for pv in rec.product_variant_ids:
                    if pv.minimum_point <= h_min:
                        h_min = pv.minimum_point
                rec.minimum_points = h_min




