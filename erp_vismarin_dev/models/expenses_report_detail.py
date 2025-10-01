from odoo import models
from datetime import datetime


class ParticularReport(models.AbstractModel):
    _name = "report.erp_vismarin_dev.report_expenses_detail"
    _description = "Expenses Report Detail"

    def calculate_given_currency(self, expenses, currency_id, margin_rate):
        expenses_list = []
        for expense in expenses:
            vals = {}
            if expense.currency_id.name == "TRY":
                currency_in_expense_date = expense.currency_id
            else:
                currency_in_expense_date = self.env["res.currency.rate"].search(
                    [
                        ("currency_id", "=", expense.currency_id.id),
                        ("name", "<=", expense.date),
                    ],
                    order="name desc",
                    limit=1,
                )

            if currency_id.name == "TRY":
                report_currency = currency_id
            else:
                report_currency = self.env["res.currency.rate"].search(
                    [
                        ("currency_id", "=", currency_id.id),
                        ("name", "<=", expense.date),
                    ],
                    order="name desc",
                    limit=1,
                )

            rate = (currency_in_expense_date.real_rate) / (report_currency.real_rate)
            vals = {
                "date": expense.date,
                "name": expense.name,
                "tax_ids": [tax.name for tax in expense.tax_ids if tax],
                "rate": rate,
                "total_amount": (expense.total_amount) * rate,
                "total_amount_with_margin": ((expense.total_amount) * rate)
                * ((100 + margin_rate) / 100),
            }
            expenses_list.append(vals)
        return expenses_list

    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model")
        docs = self.env[model].browse(self.env.context.get("active_ids", []))
        if data["employee_ids"]:
            employee_ids = self.env["hr.employee"].search(
                [("id", "in", data["employee_ids"])]
            )
        else:
            employee_ids = self.env["hr.employee"].search([])

        data["report_currency"] = self.env["res.currency"].browse(
            data["currency_id"][0]
        )

        domain = [
            ("state", "=", data["state"]),
            ("employee_id", "in", employee_ids.ids),
            ("analytic_account_id", "=", data["analytic_account_id"][0]),
            ("date", ">=", data["date_from"]),
            ("date", "<=", data["date_to"]),
        ]

        expenses = self.env["hr.expense"].search(domain)

        all_records = []
        grand_total = 0
        grand_total_with_margin = 0
        for employee in employee_ids:
            record = {}
            employee_expenses = expenses.filtered(
                lambda r: r.employee_id.id == employee.id
            )
            if len(employee_expenses) > 0:
                employee_expenses_with_currency = self.calculate_given_currency(
                    employee_expenses, data["report_currency"], data["percentage"]
                )
                record["name"] = employee.name
                record["expenses"] = []
                total = 0
                for expense in employee_expenses_with_currency:
                    vals = {
                        "date": expense["date"],
                        "name": expense["name"],
                        "tax_ids": expense["tax_ids"],
                        "total_amount": expense["total_amount"],
                        "rate": expense["rate"],
                        "total_amount_with_margin": expense["total_amount_with_margin"],
                    }
                    total += expense["total_amount"]
                    record["expenses"].append(vals)
                record["total"] = total
                grand_total += record["total"]
                record["total_with_margin"] = total * ((100 + data["percentage"]) / 100)
                grand_total_with_margin += record["total_with_margin"]
                all_records.append(record)

        data["grand_total"] = grand_total
        data["grand_total_with_margin"] = grand_total_with_margin

        return {
            "doc_ids": docids,
            "docs": docs,
            "data": data,
            "created_by": self.env.user.name,
            "report_time": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            "records": all_records,
        }
