from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand = fields.Char(related='product_tmpl_id.brand', store=True)

    #one2many reward_ids = fields.One2Many 'loyalty.reward' ('product.product', string='Gift Product', help='The product given as a reward')
    #minum point è computato dalla one2many

    reward_ids = fields.One2many('loyalty.reward', 'gift_product_id', string="Related Reward Program")

    minimum_point = fields.Float(string='Minimum Point', compute='_compute_minimum_point')

    @api.depends("reward_ids")
    def _compute_minimum_point(self):
        for rec in self:
            if len(rec.reward_ids) > 0:
                h_min = rec.reward_ids[0].minimum_points
                for rew in rec.reward_ids:
                    if rew.minimum_points < h_min:
                        h_min = rew.minimum_points
                rec.minimum_point = h_min
            else:
                rec.minimum_point = False




