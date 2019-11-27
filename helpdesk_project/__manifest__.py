# -*- coding: utf-8 -*-
{
    'name': "helpdesk_project",

    'summary': """
        Link between project and helpdesk module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['project', 'helpdesk_mgmt'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/helpdesk/helpdesk_ticket_view.xml',
        # 'views/templates.xml',
    ],
}
