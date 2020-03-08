# -*- coding: utf-8 -*-
{
    'name': "helpdesk_project",

    'summary': """
        Link between project and helpdesk module""",

    'description': """
        Link between project and helpdesk module
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    'category': 'Helpdesk',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['project', 'helpdesk_mgmt'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'views/helpdesk/helpdesk_ticket_view.xml',
        'views/helpdesk/helpdesk_ticket_channel_view.xml',
        'views/project/project_task_view.xml',
    ],
}
