from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError


class WizardExpensesReport(models.TransientModel):
    _name = "vm.expenses.report.wizard"
    _description = "Expenses Report"

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", default=fields.Date.today, required=True)
    employee_ids = fields.Many2many("hr.employee", string="Employees")
    state = fields.Selection(
        [
            ("draft", "To Submit"),
            ("reported", "Submitted"),
            ("approved", "Approved"),
            ("done", "Paid"),
            ("refused", "Refused"),
        ],
        string="Status",
        default="draft",
    )
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        readonly=True,
        states={"draft": [("readonly", False)], "refused": [("readonly", False)]},
        default=lambda self: self.env.company,
    )

    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )

    analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Protocol", check_company=True, required=True
    )

    percentage = fields.Float("Profit Margin (%)", default=0.0)

    @api.constrains("date_from", "date_to")
    def check_dates(self):
        for record in self:
            if record.date_from > record.date_to:
                raise ValidationError("End Date cannot be set before Start Date.")

    @api.constrains("percentage")
    def _constraint_percentage(self):
        for record in self:
            if not (0.0 <= record.percentage <= 100.0):
                raise UserError("Percentage must be between 0 and 100")

    def report_pdf(self):
        template = self.env.ref("erp_vismarin_dev.report_expenses_detail")
        data = self.read(
            [
                "date_from",
                "date_to",
                "employee_ids",
                "state",
                "analytic_account_id",
                "currency_id",
                "percentage",
            ]
        )[0]
        return template.report_action(self, data=data)
