from odoo import models, fields, api


class VmProjectManager(models.Model):
    _name = "vm.project.manager"
    _description = "Project Managers"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Name", required=True)
    surname = fields.Char("Surname", required=True)
    phone = fields.Char("Phone")
    email = fields.Char("Email")

    _sql_constraints = [
        (
            "unique_project_manager",
            "unique(name,surname)",
            "This record already exists!",
        )
    ]

    @api.depends("name", "surname")
    def name_get(self):
        res = []
        for record in self:
            label = record.name + " " + record.surname
            res.append((record.id, label))
        return res
