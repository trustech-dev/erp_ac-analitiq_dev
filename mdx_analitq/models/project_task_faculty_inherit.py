from odoo import models, fields


class ProjectProjectTaskInherit(models.Model):
    _inherit = "project.task"

    faculty_id = fields.Many2one("vm.faculty", string="Faculty")
    country_id = fields.Many2one(
        string="Country",
        comodel_name="res.country",
        required=True,
        default=lambda x: x.env.company.country_id.id,
        help="Country for which this report is available.",
    )
    state_id = fields.Many2one(
        "res.country.state", string="State", domain="[('country_id.code', '=', 'TR')]"
    )
    site_employee_id = fields.Many2one(
        "vm.site.employee",
        string="CRA",
        required=True,
        domain="[('employee_type', '=', 'cra')]",
    )
    site_employee_id_pi = fields.Many2many(
        "vm.site.employee",
        string="PI",
        required=True,
        domain="[('employee_type', '=', 'pi')]",
    )

    backup_sc_id = fields.Many2one(
        "res.users", string="Backup SC", index=True, tracking=True
    )
    unblinded_sc_id = fields.Many2one(
        "res.users", string="Unblinded SC", index=True, tracking=True
    )
    blinded_sc_id = fields.Many2one(
        "res.users", string="Blinded SC", index=True, tracking=True
    )

    date_siv = fields.Date("SIV", tracking=True)
    date_cov = fields.Date("COV", tracking=True)

    effective_date = fields.Date("Effective Date", tracking=True)
    last_invoice_date = fields.Date("Last Invoice Date", tracking=True)
    qty_1 = fields.Float("QTY1", tracking=True)
    qty_2 = fields.Float("QTY2.1", tracking=True)
    qty_2_date = fields.Date("QTY2 Date", tracking=True)
    qty_2_2 = fields.Float("QTY2.2", tracking=True)
    qty_3 = fields.Float("QTY3", tracking=True)
    qty_4 = fields.Float("QTY4", tracking=True)
    qty_4_valid_date = fields.Date("QTY4 Valid Date", tracking=True)
    price_1 = fields.Float("Price1", tracking=True)
    price_2 = fields.Float("Price2", tracking=True)
    price_currency_id = fields.Many2one(
        comodel_name="res.currency", string="Currency", help="The payment's currency."
    )
    agreement_status = fields.Selection(
        [("master", "Master"), ("ready", "Ready"), ("pending", "Pending")],
        "Agreement Status",
        tracking=True,
    )
    effective_method = fields.Selection(
        [
            ("siv", "SIV"),
            ("aggrement_date", "Agreement Date"),
            ("sc_approve", "SC Approve"),
        ],
        "Effective Method",
        tracking=True,
    )
    service_type = fields.Selection(
        [("fte", "FTE"), ("fte2", "FTE2"), ("sle", "SLE"), ("tbe", "TBE")],
        "Service Type",
        tracking=True,
    )
    last_billable_date = fields.Date("Last Billable Date", tracking=True)

    quotation_count = fields.Integer(compute="compute_count_quotation")

    def compute_count_quotation(self):
        quotations = self.env["sale.order.line"].search([("task_id", "=", self.id)])
        if quotations:
            quotation_list = set()
            for quotation in quotations:
                quotation_list.add(quotation.id)
            self.quotation_count = len(quotation_list)
        else:
            self.quotation_count = 0

    def get_quotation_list(self):
        quotations = self.env["sale.order.line"].search([("task_id", "=", self.id)])
        quotation_list = set()
        for quotation in quotations:
            quotation_list.add(quotation.id)

        if len(quotation_list) > 0:
            quotations = self.env["sale.order.line"].search([("task_id", "=", self.id)])
            quotation_list = set()
            for quotation in quotations:
                quotation_list.add(quotation.id)

            action = self.env.ref("mdx_analitq.open_view_sale_order_line").read()[0]
            action["domain"] = [("id", "in", list(quotation_list))]
            return action
        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "type": "warning",
                    "message": "There is no sale order line ",
                    "sticky": False,
                },
            }

    def action_url(self):
        return {"type": "ir.actions.act_url"}
