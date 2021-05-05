from odoo import fields, models, api, _
from odoo.exceptions import UserError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    payment_term_id = fields.Many2one('account.payment.term')
