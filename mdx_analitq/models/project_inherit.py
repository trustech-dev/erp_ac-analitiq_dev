from odoo import models, fields


class ProjectInherit(models.Model):
    _inherit = "project.project"

    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Analytic Account", check_company=True
    )

    # This will now work because project_id exists in account.analytic.line
    analytic_line_ids = fields.One2many(
        "account.analytic.line", "project_id", string="Analytic Time Lines"
    )
    project_responsible_id = fields.Many2one(
        "res.users",
        string="Project Responsible",
        tracking=True,
        domain="[('share', '=', False)]",  # Only internal users, no portal users
        help="Person responsible for overall project management",
    )
