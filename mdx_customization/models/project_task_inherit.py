import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class TaskInherit(models.Model):
    _inherit = "project.task"

    site_id = fields.Many2one(
        comodel_name="res.partner",
        string="Site Name",
        domain=[("is_site", "=", True)],
        context={"default_is_site": True},
        required=True,
    )

    project_code = fields.Char(related="project_id.project_code", string="Project Code")

    site_patient_payable_amount = fields.Float(
        string="Patient Payable Amount",
        tracking=True,
    )

    site_patient_payable_amount_currency_id = fields.Many2one(
        comodel_name="mdx.static.parameter",
        string="Currency",
        help="The payment's currency.",
        tracking=True,
        default=lambda self: self._get_default_currency_for_task(),
    )

    def _get_default_currency_for_task(self):
        try:
            project_id = self.env.context.get(
                "default_project_id"
            ) or self.env.context.get("active_id")

            if project_id:
                project = self.env["project.project"].browse(project_id)
                if project.project_patient_payable_amount_currency_id:
                    return project.project_patient_payable_amount_currency_id.id

            # Fallback to TRY
            try_currency = self.env["res.currency"].search(
                [("name", "=", "USD")], limit=1
            )
            return try_currency.id if try_currency else False

        except Exception as e:
            _logger.warning(f"Error in _get_default_currency_for_task: {e}")
            return False

    @api.onchange("project_id")
    def _onchange_project_id_set_currency(self):
        """Update currency when project is changed"""
        if (
            self.project_id
            and self.project_id.project_patient_payable_amount_currency_id
        ):
            self.site_patient_payable_amount_currency_id = (
                self.project_id.project_patient_payable_amount_currency_id
            )
