import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ProjectInherit(models.Model):
    _inherit = "project.project"

    project_code = fields.Char(
        string="Project Code",
        tracking=True,
    )

    project_patient_payable_amount = fields.Float(
        string="Patient Payable Amount",
        tracking=True,
    )
    project_patient_payable_amount_currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Project Currency",
        help="The payment's currency.",
        tracking=True,
        default=lambda self: self._get_default_currency(),
    )

    service_fee = fields.Float(
        string="Service Fee (%)",
        help="Service fee percentage (e.g., 10 for 10%)",
        digits=(5, 2),
        tracking=True,
        default=0.0,
    )

    def _get_default_currency(self):
        """Get TRY currency if exists, otherwise USD, otherwise company currency"""
        try:
            currency = self.env["res.currency"].search([("name", "=", "TRY")], limit=1)
            if currency:
                return currency.id

            currency = self.env["res.currency"].search([("name", "=", "USD")], limit=1)
            if currency:
                return currency.id

            return self.env.company.currency_id.id

        except Exception as e:
            _logger.error(f"Error getting default currency: {e}")
            return self.env.company.currency_id.id

    @api.constrains("service_fee")
    def _check_service_fee(self):
        for record in self:
            if record.service_fee < 0:
                raise ValidationError("Service fee cannot be negative!")
            if record.service_fee > 100:
                raise ValidationError("Service fee cannot exceed 100%!")
