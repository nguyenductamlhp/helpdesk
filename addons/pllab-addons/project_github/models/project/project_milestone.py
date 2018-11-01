# -*- encoding: utf-8 -*-
###############################################################################
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>               #
###############################################################################

import urllib.request
from urllib.request import urlopen
from github import Github

from odoo import api, fields, models
from odoo.exceptions import Warning


class ProjectMilestone(models.Model):
    _name = 'project.milestone'
    _order = 'name DESC'

    name = fields.Char('Milestone', required=True)
    number = fields.Integer('Number', required=True)
    project_id = fields.Many2one(
        'project.project', 'Project', required=True)
    description = fields.Text('Description')
    due_date = fields.Date('Due Date')
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('closed', 'Closed')
        ]
    )
