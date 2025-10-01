{
    "name": "erp_vismarin_dev",
    "summary": """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    "description": """
        Long description of module's purpose 
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "hr",
        "hr_expense",
        "hr_timesheet",
        "maintenance",
    ],
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/hr_employee_inherit_view.xml",
        "views/maintenance_equipment_inherit_view.xml",
        "views/vm_faculty_view.xml",
        "views/vm_patient_view.xml",
        "views/vm_site_employee_pi_view.xml",
        "views/vm_site_employee_cra_view.xml",
        "views/vm_visit_view.xml",
        "views/vm_indication_view.xml",
        "views/project_task_faculty_inherit_view.xml",
        "views/account_analytic_line_inherit_view.xml",
        # "views/account_move_inherit_view.xml",
        "views/hr_expense_sheet_inherit_view.xml",
        "views/vm_project_manager_view.xml",
        "views/project_views_inherit.xml",
        "views/vm_project_tracking.xml",
        "wizard/expenses_report_wizard_view.xml",
        "wizard/expenses_report_wizard_view.xml",
        "report/expenses_report_template.xml",
        "report/hr_expense_report_inherit.xml",
        "menu/menu.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
    "installable": True,
}
