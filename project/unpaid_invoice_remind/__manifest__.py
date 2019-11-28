# -*- coding: utf-8 -*-
{
    'name': "Unpaid Invoice Remind",

    'summary': """
        Send email to remind late paiding invoice""",

    'description': """
        Send email to remind late paiding invoice
    """,

    'author': "nguyenductamlhp",
    'website': "http://www.pllabvn.com",

    'category': 'Uncategorized',
    'version': '11.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account_invoicing'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
    ],
}
