from odoo import models, fields, api


class AnalyticAccountLineInherit(models.Model):
    _inherit = "account.analytic.line"

    task_id = fields.Many2one(
        "project.task",
        "Sites",
        compute="_compute_task_id",
        store=True,
        readonly=False,
        index=True,
        required=True,
        domain="[('company_id', '=', company_id), ('project_id.allow_timesheets', '=', True), ('project_id', '=?', project_id)]",
    )
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        related="task_id.project_id",
        store=True,
        readonly=True,
    )
    patient_id = fields.Many2one("vm.patient", string="Patients")
    visit_type_id = fields.Many2one(
        "vm.visit.type", string="Visit Type", required=False
    )
    visit_type_name = fields.Char("Visit Name", related="visit_type_id.name")
    visit_no = fields.Char(
        string="Visit Number",
        required=True,
    )

    planned_date = fields.Date(string="Planned Date")

    @api.onchange("task_id")
    def _onchange_task_id(self):
        for rec in self:
            rec.patient_id = False

    @api.onchange("visit_no")
    def _onchange_visit_no(self):
        if self.visit_no:
            self.visit_no = self.visit_no.upper()

    @api.onchange("visit_type_name")
    def _onchange_visit_type_name(self):
        if self.visit_type_name != "PATIENT VISIT":
            self.visit_no = "NA"
        else:
            self.visit_no = False
