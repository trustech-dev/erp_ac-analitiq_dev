from odoo import models, fields


class ProjectInherit(models.Model):
    _inherit = "project.project"

    indication_id = fields.Many2one("vm.indication", string="Indication")
    project_responsible_id = fields.Many2one(
        "res.users", string="Project Responsible", tracking=True
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account", check_company=True
    )
