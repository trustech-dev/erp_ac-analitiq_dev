from odoo import models, fields


class TherapeuticArea(models.Model):
    _name = "therapeutic.area"
    _inherit = "mail.thread"
    _description = "Therapeutic Area"

    name = fields.Char(
        "Therapeutic Area",
        required=True,
        tracking=True,
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [("unique_name", "unique(name)", "Name should be unique!")]


class Indication(models.Model):
    _name = "indication"
    _description = "Indication"
    _order = "name"

    name = fields.Char(string="Indication", required=True, tracking=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ("unique_name", "unique(name)", "Indication name must be unique!")
    ]
