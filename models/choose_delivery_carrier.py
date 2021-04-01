from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    def button_confirm(self):
        res = super(ChooseDeliveryCarrier, self).button_confirm()
        self.order_id.remove_tax_from_delivery()
        return res
