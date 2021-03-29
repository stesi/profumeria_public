# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    config_id = fields.Many2one(store=True)

    @api.model
    def fields_get(self, fields=None, attributes=None):
        fields_to_hide = ['payment_ids']
        res = super(PosOrder, self).fields_get(fields,attributes)
        for field in fields_to_hide:
            res[field]['searchable'] = False
        return res