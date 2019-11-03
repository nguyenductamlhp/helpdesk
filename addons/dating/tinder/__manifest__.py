# -*- coding: utf-8 -*-
{
    'name': "tinder",

    'summary': """
        Auto interactive (swipe, send message) with tinder""",

    'description': """
        Auto interactive (swipe, send message) with tinder:
    - Auto like tinder
    - Send message
    ....
    - Create partner from people (work on separate server)
    """,

    'author': "PL Lab",
    'website': "http://www.pllabvn.com",

    'category': 'Uncategorized',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}