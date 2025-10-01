from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging


_logger = logging.getLogger(__name__)


class HrExpense(models.Model):
    _inherit = "hr.expense"

    def _default_analytic_account(self):
        analytic_account_id = self._context.get("analytic_account_id", False)
        if analytic_account_id:
            return self.env["account.analytic.account"].browse(analytic_account_id)
        return False

    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Protocol",
        check_company=True,
        default=_default_analytic_account,
    )
    patient_id = fields.Many2one(
        "vm.patient",
        string="Patient",
        domain=lambda self: "[('task_id', '=', %s)]"
        % self._context.get("task_id", False)
        if self._context.get("task_id", False)
        else "[]",
    )
    investigator_id = fields.Many2one(
        "vm.site.employee", string="Investigator", related="patient_id.site_employee_id"
    )
    payment_mode = fields.Selection(
        [("own_account", "Employee"), ("company_account", "Company(Advance)")],
        default="own_account",
        tracking=True,
        states={
            "done": [("readonly", True)],
            "approved": [("readonly", True)],
            "reported": [("readonly", True)],
        },
        string="Paid By",
    )
    is_blinded = fields.Boolean("Is Blinded?", tracking=True, help="Fiş körlenmiş mi?")

    visit_date = fields.Date(
        "Visit Date", required=True, default=fields.Date.context_today
    )

    @api.depends("product_id", "company_id")
    def _compute_from_product_id_company_id(self):
        for expense in self.filtered("product_id"):
            expense = expense.with_company(expense.company_id)
            if not expense.attachment_number or (
                expense.attachment_number and not expense.unit_amount
            ):
                expense.unit_amount = expense.product_id.price_compute(
                    "standard_price"
                )[expense.product_id.id]
            expense.product_uom_id = expense.product_id.uom_id
            expense.tax_ids = expense.product_id.supplier_taxes_id.filtered(
                lambda tax: tax.company_id == expense.company_id
            )  # taxes only from the same company
            account = expense.product_id.product_tmpl_id._get_product_accounts()[
                "expense"
            ]
            if account:
                expense.account_id = account

    def get_attachments(self):
        domain = [("res_id", "=", self.id), ("res_model", "=", "hr.expense")]
        attachments = self.env["ir.attachment"].sudo().search(domain)
        return attachments


class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet"

    project_id = fields.Many2one("project.project", string="Protocol", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Customer", related="project_id.partner_id"
    )
    task_id = fields.Many2one(
        "project.task",
        "Site",
        required=True,
        domain="[('company_id', '=', company_id), ('project_id', '=', project_id)]",
    )
    site_employee_id = fields.Many2one(
        "vm.site.employee", string="CRA", related="task_id.site_employee_id"
    )
    analytic_account = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        compute="_compute_analytic_account",
        store=True,
    )

    user_id = fields.Many2one(
        "res.users",
        "Manager",
        compute="_compute_from_employee_id",
        store=True,
        readonly=True,
        copy=False,
        states={"draft": [("readonly", True)]},
        tracking=True,
        domain=lambda self: [
            (
                "groups_id",
                "in",
                self.env.ref("hr_expense.group_hr_expense_team_approver").id,
            )
        ],
    )
    is_approved = fields.Selection(
        [
            ("yes", "Yes"),
            ("no", "No"),
            ("na", "NA"),
        ],
        string="The payments on this form are consistent with the payment approved by the sponsor or ethics committee per patient visit",
        required=True,
    )
    payment_status = fields.Selection(
        [
            ("payable", "Payable"),
            ("invoice", "Invoice"),
            ("payment", "Payment"),
            ("invoice/payment", "Invoice&Payment"),
        ],
        string="Payment Status",
        tracking=True,
        default="payable",
    )
    patient_payable_amount = fields.Monetary(
        "Patient Payable Amount", required=True, help="Hasta Hakediş Tutarı"
    )
    expense_type = fields.Selection(
        [
            ("sc_expense", "SC Expense"),
            ("patient_expense", "Patient Expense"),
            ("pharmacy_expense", "Pharmacy Expense"),
        ],
        string="Expense Type",
        tracking=True,
        required=True,
    )

    note = fields.Text(string="Note")

    @api.depends("project_id")
    def _compute_analytic_account(self):
        for record in self:
            # Check if project has analytic_account_id, if not, create one
            if record.project_id and not record.project_id.analytic_account_id:
                # Create analytic account if needed
                analytic_account = self.env["account.analytic.account"].create(
                    {
                        "name": record.project_id.name,
                        "company_id": record.company_id.id,
                    }
                )
                record.project_id.analytic_account_id = analytic_account
            record.analytic_account = record.project_id.analytic_account_id

    def get_attachments(self):
        domain = [("res_id", "=", self.id), ("res_model", "=", "hr.expense.sheet")]
        attachments = self.env["ir.attachment"].sudo().search(domain)
        return attachments

    @api.onchange("project_id")
    def _onchange_project_id(self):
        for rec in self:
            rec.task_id = False

    def get_attachment_status(self):
        domain = [
            ("id", "=", self.message_main_attachment_id.id),
            ("res_model", "=", "hr.expense.sheet"),
        ]
        domain2 = [
            ("res_id", "in", self.expense_line_ids.ids),
            ("res_model", "=", "hr.expense"),
        ]
        attachments_count = self.env["ir.attachment"].sudo().search_count(domain)
        attachments_count2 = self.env["ir.attachment"].sudo().search_count(domain2)
        if attachments_count > 0 or attachments_count2 > 0:
            return True
        return False

    def control_attachment_status_expense_line(self):
        domain = [
            ("res_id", "in", self.expense_line_ids.ids),
            ("res_model", "=", "hr.expense"),
        ]
        attachments_count = self.env["ir.attachment"].sudo().search_count(domain)
        if attachments_count > 0:
            return True
        return False

    def write(self, vals):
        # Grup group_medex_payment_status değilse payment status değişmesin
        if vals.get("payment_status"):
            if bool(vals["payment_status"]) and not bool(
                self.env.user.has_group("erp_vismarin_dev.group_medex_payment_status")
            ):
                raise UserError(_("You cannot edit the Payment Status."))
        if any(state == "draft" for state in set(self.mapped("state"))):
            return super().write(vals)
        elif self.env.user.has_group("hr_expense.group_hr_expense_manager"):
            return super().write(vals)
        else:
            raise UserError(_("No edit in this state"))

    def action_submit_sheet(self):
        attachments = self.env["ir.attachment"].search([("res_id", "=", self.id)])
        attachment_count = self.env["ir.attachment"].search_count(
            [("res_id", "=", self.id)]
        )
        if len(self.expense_line_ids.ids) == 0:
            raise UserError(_("Expense line cannot be empty."))
        if attachment_count > 0:
            for attachment in attachments:
                file_category = attachment.mimetype.split("/")[0]
                if file_category != "image":
                    raise UserError(_("Upload receipt images in image format."))
            super().action_submit_sheet()
        else:
            raise UserError("Add receipt images.")
