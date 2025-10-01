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
    site_employee_id_pi = fields.Many2one(
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

            action = self.env.ref("erp_vismarin_dev.open_view_sale_order_line").read()[
                0
            ]
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
