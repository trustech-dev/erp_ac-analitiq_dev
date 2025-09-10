# -*- coding: utf-8 -*-
{
    "name": "mdx_analitiq",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose 
    """,
    "author": "Medex",
    "website": "http://www.yourcompany.com",
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "hr",
        "sale",
        "sale_project",
        "hr_expense",
        "hr_timesheet",
        "maintenance",
        "portal",
        "fleet",
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/account_analytic_line_inherit_view.xml",
        "views/hr_employee_inherit_view.xml",
        "views/hr_expense_sheet_inherit_view.xml",
        "views/project_views_inherit.xml",
        "views/vm_patient_view.xml",
        "views/vm_project_manager_view.xml",
        "views/vm_project_tracking.xml",
        "views/vm_site_employee_pi_view.xml",
        "views/vm_site_employee_cra_view.xml",
        "views/vm_visit_view.xml",
        "report/hr_expense_report_inherit.xml",
        "menu/menu.xml",
    ],
}
