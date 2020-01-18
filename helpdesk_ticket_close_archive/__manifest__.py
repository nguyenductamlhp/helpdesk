# -*- coding: utf-8 -*-
{
    'name': "helpdesk_ticket_close_archive",

    'summary': """Archive ticket which move to stage which marked closed""",

    'description': """
- Ticket which move to stage closed will be archive
- Ticket which move out od stage closed will be unarchive
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    'category': 'Helpdesk',
    'version': '11.0.1',

    'depends': ['base', 'helpdesk_mgmt'],

    # always loaded
    'data': [
        'views/helpdesk/helpdesk_ticket_view.xml',
    ],
}