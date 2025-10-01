from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VmVisitType(models.Model):
    _name = "vm.visit.type"
    _description = "Visit Type"

    name = fields.Char("Name")

    _sql_constraints = [
        ("unique_name", "unique(name)", "Name should be unique per patients!")
    ]

    @api.constrains("name")
    def _check_name(self):
        for rec in self:
            if not rec.name:
                raise ValidationError("Name field can not be empty!")
