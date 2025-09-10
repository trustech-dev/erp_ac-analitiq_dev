from odoo import models, fields, api


class VmPatient(models.Model):
    _name = 'vm.patient'
    _description = 'Patients'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Code")
    description = fields.Text("Description")
    site_employee_id = fields.Many2one('vm.site.employee', 'PI Name', required=True,  domain="[('employee_type', '=', 'pi')]")
    date = fields.Date(string='Date', default=fields.Date.context_today)
    project_id = fields.Many2one('project.project', 'Project', required=True)
    task_id = fields.Many2one('project.task', 'Site', required=True)


