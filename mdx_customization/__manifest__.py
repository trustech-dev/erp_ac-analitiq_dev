{
    "name": "mdx_customization",
    "author": "medex",
    "installable": True,
    "application": False,
    "auto_install": False,
    "depends": [
        "project",
        "contacts",
    ],
    "data": [
        "data/site_no_medex_sequence.xml",
        "views/project_view_inherit.xml",
        "views/res_partner_view_inherit.xml",
        "views/therapautic_view.xml",
        "security/ir.model.access.csv",
    ],
    "license": "LGPL-3",
}
