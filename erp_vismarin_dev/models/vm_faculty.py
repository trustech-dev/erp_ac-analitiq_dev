from odoo import models, fields


class VmUniversity(models.Model):
    _name = "vm.university"
    _description = "Universities"

    name = fields.Char("Name", required=True)


class VmDepartment(models.Model):
    _name = "vm.department"
    _description = "Departments"

    name = fields.Char("Name", required=True)


class VmFaculty(models.Model):
    _name = "vm.faculty"
    _description = "Faculties"
    _rec_name = "name"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    title = fields.Many2one("res.partner.title", "Title")
    name = fields.Char("Name", size=128, required=True)
    phone = fields.Char("Phone")
    mail = fields.Char("Mail")
    university = fields.Many2one("vm.university", "University", required=True)
    department = fields.Many2one("vm.department", "Department", required=True)
