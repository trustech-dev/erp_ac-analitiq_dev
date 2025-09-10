from odoo import models, fields, api


class VMProjectManager(models.Model):
    _name = "vm.project.manager"
    _description = "Project Manager"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", required=True, tracking=True)

    surname = fields.Char(string="Surname", required=True, tracking=True)

    phone = fields.Char(string="Phone", tracking=True)

    email = fields.Char(string="Email", tracking=True)

    # Optional: Computed field for full name
    full_name = fields.Char(
        string="Full Name", compute="_compute_full_name", store=True
    )

    @api.depends("name", "surname")
    def _compute_full_name(self):
        for manager in self:
            manager.full_name = f"{manager.name or ''} {manager.surname or ''}".strip()

    # Optional: Add name search functionality
    def name_get(self):
        result = []
        for manager in self:
            name = (
                f"{manager.name} {manager.surname}"
                if manager.name and manager.surname
                else manager.name or manager.surname
            )
            result.append((manager.id, name))
        return result

    # Optional: Add constraints
    _sql_constraints = [
        (
            "email_unique",
            "UNIQUE(email)",
            "Email must be unique for each project manager.",
        ),
    ]
