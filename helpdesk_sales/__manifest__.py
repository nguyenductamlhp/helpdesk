# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Sales",
    'summary': """
Sale support service on helpdesk ticket
""",
    'description': """
Features:
- Add estimation by hour on helpdesk ticket
- Create Sale order from helpdesk ticket
    """,
    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    'category': 'Helpdesk',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['helpdesk_mgmt', 'sale_management'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/helpdesk/helpdesk_ticket_view.xml',
    ],
}