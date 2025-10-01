from odoo import models, fields, api


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    name = fields.Char(compute="")

    @api.onchange("name", "highest_name")
    def _onchange_name_warning(self):
        return 0
