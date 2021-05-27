from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResUsers(models.Model):
    _inherit = 'res.users'

    user_birthday = fields.Date()
