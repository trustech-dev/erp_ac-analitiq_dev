from odoo import models, fields


class MaintenanceEquipmetInherit(models.Model):
    _inherit = "maintenance.equipment"

    project_id = fields.Many2one("project.project", string="Project")
    task_id = fields.Many2one(
        "project.task", string="Task", domain="[('project_id', '=', project_id)]"
    )
