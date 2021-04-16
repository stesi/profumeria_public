from odoo import api, models, fields

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    countersign = fields.Boolean(string="Countersign",default=False)
