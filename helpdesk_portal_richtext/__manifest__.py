# -*- coding: utf-8 -*-
{
    'name': "Helpdesk Portal Richtext",

    'summary': """
        Integrate richtext editer in portal""",

    'description': """
        Integrate richtext editer in portal
    """,

    'author': "Nguyen Duc Tam <nguyenductamlhp@gmail.com>",
    'website': "http://www.pllabvn.com",

    'category': 'Helpdesk',
    'version': '11.0.1',

    'depends': ['base', 'helpdesk_mgmt'],

    # always loaded
    'data': [
        'views/templates.xml',
    ],
}