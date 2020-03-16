# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Tickets Merging",

    'summary': """
        Merge multiple helpdesk tickets""",

    'description': """
        Merge multiple helpdesk tickets
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    'category': 'Helpdesk',
    'version': '11.0.1',

    'depends': ['base', 'helpdesk_mgmt'],

    'data': [
        'views/helpdesk_ticket_view.xml',
        'wizard/merge_tickets_wizard_view.xml',
    ],
}
