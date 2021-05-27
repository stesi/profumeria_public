from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    pos_ids = fields.One2many('pos.order', 'partner_id', domain=[('state', 'not in', ['cancel', 'draft'])])
    sale_ids = fields.One2many('sale.order', 'partner_id', domain=[('state', 'not in', ['cancel', 'draft'])])

    amount_total = fields.Float(compute='_compute_last_purchase_date', store=True)
    last_purchase_date = fields.Datetime(compute='_compute_last_purchase_date', store=True)
    number_of_completed_pos_ids = fields.Integer(compute='_compute_last_purchase_date', store=True,
                                                 string="Number of Pos Orders")
    number_of_completed_sale_ids = fields.Integer(compute='_compute_last_purchase_date', store=True,
                                                  string="Number of Sale Orders")
    birthday = fields.Date()

    @api.depends('pos_ids', 'sale_ids')
    def _compute_last_purchase_date(self):
        for partner in self:
            partner.last_purchase_date = False
            total_purchases = 0
            if len(partner.pos_ids) > 0:
                partner.last_purchase_date = \
                partner.pos_ids.sorted(lambda l: l.date_order, reverse=True).mapped('date_order')[0]
                total_purchases += sum(partner.pos_ids.mapped('amount_total'))
            if len(partner.sale_ids) > 0:
                sale_date = partner.sale_ids.sorted(lambda l: l.date_order, reverse=True).mapped('date_order')[0]
                total_purchases += sum(partner.sale_ids.mapped('amount_total'))
                if not partner.last_purchase_date or sale_date > partner.last_purchase_date:
                    partner.last_purchase_date = sale_date

            partner.number_of_completed_pos_ids = len(partner.pos_ids)
            partner.number_of_completed_sale_ids = len(partner.sale_ids)
            partner.amount_total = total_purchases
