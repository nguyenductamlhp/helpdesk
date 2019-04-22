# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>
{
    'name': 'Hostel Management',
    'summary': """ Manage hostel """,
    'version': '11.0.0',
    'category': 'Other',
    'author': 'nguyenductamlhp',
    'contributors': ['Nguyen Duc Tam <nguyenductamlhp@gmail.com>'],
    'depends': [
        'base', 'product',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/base/res_partner_view.xml',
        'views/hostel/hostel_room_view.xml',
        'views/hostel/hostel_invoice_view.xml',
        # 'views/project/project_milestone_view.xml',

        'menu/hostel_menu.xml',
    ],
    'installable': True,
    'application': True,
}
