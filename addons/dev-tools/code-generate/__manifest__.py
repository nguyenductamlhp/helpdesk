# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>
{
    'name': 'Code Generate',
    'summary': """ Support develop odoo """,
    'version': '11.0.0',
    'category': 'Development Tools',
    'author': 'nguyenductamlhp',
    'contributors': ['Nguyen Duc Tam <nguyenductamlhp@gmail.com>'],
    'depends': [
        'base', 'project',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views
        'views/code_model_view.xml',

        # 'menu/
        'menu/dev_tool_menu.xml',
    ],
    'installable': True,
    'application': True,
}
