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
    patient_id = fields.Many2one("vm.patient", string="Patients")
    visit_type_id = fields.Many2one(
        "vm.visit.type", string="Visit Type", required=False
    )
    visit_type_name = fields.Char("Visit Name", related="visit_type_id.name")
    visit_no = fields.Char(
        string="Visit Number",
        required=True,
    )

    backup_sc_id = fields.Many2one(
        "res.users",
        string="Backup SC",
        index=True,
        tracking=True,
        related="task_id.backup_sc_id",  # Link to the task field
        store=True,
    )
    unblinded_sc_id = fields.Many2one(
        "res.users",
        string="Unblinded SC",
        index=True,
        tracking=True,
        related="task_id.unblinded_sc_id",  # Link to the task field
        store=True,
    )
    blinded_sc_id = fields.Many2one(
        "res.users",
        string="Blinded SC",
        index=True,
        tracking=True,
        related="task_id.blinded_sc_id",  # Link to the task field
        store=True,
    )
    faculty_id = fields.Many2one(
        "vm.faculty",
        string="Faculty",
        related="task_id.faculty_id",  # Link to the task field
        store=True,
    )
    site_employee_id = fields.Many2one(
        "vm.site.employee",
        string="CRA",
        related="task_id.site_employee_id",  # Link to the task field
        store=True,
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

    @api.depends("project_id", "patient_id")
    def _compute_task_id(self):
        for record in self:
            # Add your computation logic here
            # This is just an example - adjust based on your business logic
            if record.project_id and record.patient_id:
                # Find or create task based on your logic
                record.task_id = False  # Replace with actual computation
            else:
                record.task_id = False
