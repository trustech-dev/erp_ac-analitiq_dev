import logging

from odoo import models, fields, api


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(
        selection_add=[("site", "Site")], ondelete={"site": "cascade"}
    )

    parent_id = fields.Many2one(
        "res.partner",
        domain="['|', ('is_site', '=', True), ('is_company', '=', True)]",
        string="Related Company/Site",
    )
    # company_type == Person
    person_role = fields.Selection(
        [
            ("cra", "CRA"),
            ("pi", "PI"),
            ("pharmacy", "Pharmacist"),
            ("nurse", "Study Nurse"),
            ("sub_i", "SUBI"),
        ],
        string="Person Role",
        tracking=True,
    )

    is_cra = fields.Boolean(compute="_compute_is_cra", store=True)
    is_pi = fields.Boolean(compute="_compute_is_pi", store=True)
    is_pharmacy = fields.Boolean(compute="_compute_is_pharmacy", store=True)
    is_nurse = fields.Boolean(compute="_compute_is_nurse", store=True)
    is_sub_i = fields.Boolean(compute="_compute_is_sub_i", store=True)

    therapeutic_area_ids = fields.Many2many(
        comodel_name="therapeutic.area",
        relation="partner_therapeutic_area_rel",
        column1="partner_id",
        column2="therapeutic_area_id",
        string="Therapeutic Areas",
        tracking=True,
    )

    indication_ids = fields.Many2many(
        "indication",
        relation="partner_indication_rel",
        column1="partner_id",
        column2="indication_id",
        string="Indications",
        tracking=True,
    )

    therapeutic_area_domain = fields.Boolean(
        compute="_compute_therapeutic_area_domain",
        store=False,
    )

    @api.depends("person_role", "company_type")
    def _compute_therapeutic_area_domain(self):
        """Compute field to control therapeutic area visibility"""
        for partner in self:
            _logger.warning(
                f"{partner.name} company_type is {partner.company_type}, role is :{partner.person_role}"
            )
            partner.therapeutic_area_domain = (
                partner.company_type == "person"
                and partner.person_role in ["pi", "sub_i"]
            )

    @api.depends("person_role")
    def _compute_is_cra(self):
        for partner in self:
            partner.is_cra = partner.person_role == "cra"

    @api.depends("person_role")
    def _compute_is_pi(self):
        for partner in self:
            partner.is_pi = partner.person_role == "pi"

    @api.depends("person_role")
    def _compute_is_pharmacy(self):
        for partner in self:
            partner.is_pharmacy = partner.person_role == "pharmacy"

    @api.depends("person_role")
    def _compute_is_nurse(self):
        for partner in self:
            partner.is_nurse = partner.person_role == "nurse"

    @api.depends("person_role")
    def _compute_is_sub_i(self):
        for partner in self:
            partner.is_sub_i = partner.person_role == "sub_i"

    is_sponsor = fields.Boolean(
        "Sponsor",
        tracking=True,
    )

    is_sponsor_legal_representative = fields.Boolean(
        "Sponsor Legal Representative",
        tracking=True,
    )

    is_subcontract = fields.Boolean(
        "Subcontract",
        tracking=True,
    )

    is_site = fields.Boolean(
        compute="_compute_is_site", store=True, string="Is Site", index=True
    )
    is_person = fields.Boolean(
        compute="_compute_is_person", store=True, string="Is Person", index=True
    )

    @api.depends("company_type")
    def _compute_is_site(self):
        for partner in self:
            partner.is_site = partner.company_type == "site"

    @api.depends("company_type")
    def _compute_is_person(self):
        for partner in self:
            partner.is_person = partner.company_type == "person"

    @api.depends("is_company")
    def _compute_company_type(self):
        for partner in self:
            if partner.is_site and not partner.is_company:
                partner.company_type = "site"
            elif partner.is_company and not partner.is_site:
                partner.company_type = "company"
            else:
                partner.company_type = "person"

    @api.onchange("company_type")
    def onchange_company_type(self):
        if self.company_type == "company":
            self.is_company = True
            self.is_site = False
        if self.company_type == "person":
            self.is_company = False
            self.is_site = False
        if self.company_type == "site":
            self.is_company = False
            self.is_site = True

    site_no = fields.Char(
        string="Site No",
        tracking=True,
        default="",
    )

    site_no_medex = fields.Char(
        string="Site No to Private",
        tracking=True,
        help="Unique identifier for the BI",
        default=lambda self: self.env["ir.sequence"].next_by_code("medex.site.number"),
        readonly=True,
        copy=False,
        index=True,
    )

    nda_no = fields.Char(
        string="NDA No",
        tracking=True,
    )

    nda_effective = fields.Date(
        "NDA Effective Date",
        tracking=True,
    )

    nda_end = fields.Date(
        "NDA End Date",
        tracking=True,
    )
