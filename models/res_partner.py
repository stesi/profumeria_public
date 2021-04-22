from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pos_ids = fields.One2many('pos.order','partner_id',domain=[('state','!=','cancel')])
    sale_ids = fields.One2many('sale.order','partner_id',domain=[('state','!=','cancel')])

    last_purchase_date = fields.Datetime(compute = '_compute_last_purchase_date',store=True)

    @api.depends('pos_ids','sale_ids')
    def _compute_last_purchase_date(self):
        for partner in self:
            partner.last_purchase_date = False
            if len(partner.pos_ids)>0:
                partner.last_purchase_date = partner.pos_ids.sorted(lambda l: l.date_order,reverse=True).mapped('date_order')[0]
            if len(partner.sale_ids) > 0:
                sale_date = partner.sale_ids.sorted(lambda l: l.date_order,reverse=True).mapped('date_order')[0]
                if not partner.last_purchase_date or sale_date > partner.last_purchase_date:
                    partner.last_purchase_date = sale_date
