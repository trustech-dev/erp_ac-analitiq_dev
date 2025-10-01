from odoo import models, fields, api
from odoo.exceptions import ValidationError


class VmProjectDetail(models.Model):
    _name = "vm.project.tracking"
    _description = "Project Tracking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "id desc"

    name = fields.Char("Protocol No", required=True, tracking=True)
    project_name = fields.Char("Project Name", required=True, tracking=True)
    employee_id = fields.Many2one(
        "hr.employee",
        string="Employee",
        store=True,
        required=True,
        readonly=True,
        tracking=True,
        default=lambda self: self.env.user.employee_id,
    )
    bool_primer = fields.Boolean("Primer", tracking=True)
    bool_backup = fields.Boolean("Backup", tracking=True)
    bool_blinded = fields.Boolean("Blinded", tracking=True)
    bool_unblinded = fields.Boolean("Unblinded", tracking=True)

    sponsor_name = fields.Char("Sponsor", required=True, tracking=True)
    site_name = fields.Char("Site Name", required=True, tracking=True)
    site_no = fields.Char("Site No", required=True, tracking=True)
    indication = fields.Char("Indication", required=True, tracking=True)
    site_status = fields.Selection(
        [("active", "Active"), ("passive", "Passive")],
        "Site Status",
        required=True,
        tracking=True,
    )

    date_siv = fields.Date("SIV", tracking=True)
    date_cov = fields.Date("COV", tracking=True)
    patient_admission = fields.Boolean(
        "Is patient enrollment still going on?", required=True, tracking=True
    )
    patient_count = fields.Integer(
        "Number of randomized patients", required=True, tracking=True
    )
    visit_frequency = fields.Char("Visit Frequency", tracking=True)

    pi_title = fields.Char("PI Title", required=True, tracking=True)
    pi_name = fields.Char("PI Name/Surname", required=True, tracking=True)
    pi_mobile = fields.Char("PI Mobile", required=True, tracking=True)
    pi_mail = fields.Char("PI Mail", required=True, tracking=True)

    # Odoo 16'ya geçerken alttaki 5 field subi olarak değiştirilecek.
    pi_control = fields.Selection(
        [("yes", "Yes"), ("no", "No")], string="Is there SUBI in the project?"
    )
    pi_title2 = fields.Char("SUBI Title", tracking=True)
    pi_name2 = fields.Char("SUBI Name/Surname", tracking=True)
    pi_mobile2 = fields.Char("SUBI Mobile", tracking=True)
    pi_mail2 = fields.Char("SUBI Mail", tracking=True)

    cra_name = fields.Char("CRA Name/Surname", required=True, tracking=True)
    cra_mobile = fields.Char("CRA Mobile", required=True, tracking=True)
    cra_mail = fields.Char("CRA Mail", required=True, tracking=True)

    note = fields.Text("Note", tracking=True)

    is_approved = fields.Boolean(
        "I confirm that my information is correct", tracking=True
    )

    @api.constrains("is_approved")
    def _check_is_approved(self):
        if not self.is_approved:
            raise ValidationError("Please confirm the accuracy of the data!")

    @api.constrains("pi_control")
    def _check_pi_control(self):
        if not self.pi_control:
            raise ValidationError("Is there another PI?' field can not be empty!")
