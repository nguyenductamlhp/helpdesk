# -*- coding: utf-8 -*-
{
    'name': "helpdesk_ticket_portal_image",

    'summary': """
        Show image on helpdesk ticket portal""",

    'description': """
        Show image on helpdesk ticket portal
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Helpdesk',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'helpdesk_mgmt'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/templates.xml',
    ],
}