from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand = fields.Char(related='product_tmpl_id.brand', store=True)

    #one2many reward_ids = fields.One2Many 'loyalty.reward' ('product.product', string='Gift Product', help='The product given as a reward')
    #minum point è computato dalla one2many