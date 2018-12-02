# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>
{
    'name': 'Project Github Integration',
    'summary': """ Integrate github with feature of projects """,
    'version': '11.0.1',
    'category': 'Project',
    'author': 'nguyenductamlhp',
    'contributors': ['Nguyen Duc Tam <nguyenductamlhp@gmail.com>'],
    'depends': [
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/base/res_partner_view.xml',
        'views/project/project_tasks_view.xml',
        'views/project/project_project_view.xml',
        'views/project/project_milestone_view.xml',

        'menu/project_menu.xml',
    ],
    'installable': True,
    'application': True,
}
