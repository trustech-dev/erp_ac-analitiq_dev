from odoo import models, fields, api


class VmSiteEmployee(models.Model):
    _name = 'vm.site.employee'
    _description = 'Site Employees'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Name", required=True)
    surname = fields.Char("Surname", required=True)
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    employee_type = fields.Selection(
        [('pi', 'PI'),
        ('cra', 'CRA')], required=True, string="Site Employee Type" )
    


    _sql_constraints = [
        ('unique_site_employee',
         'unique(name,surname,employee_type)', 'This record already exists!')]



    @api.depends('name', 'surname')
    def name_get(self):
        res = []
        for record in self:
            label = record.name + ' ' + record.surname
            res.append((record.id, label))
        return res