# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import models, fields, api


class GithubMilestone(models.Model):
    _name = 'github.milestone'

    name = fields.Char('Milestone', required=True)
    number = fields.Integer('Number', required=True)
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('close', 'Close')
        ]
    )
    due_date = fields.Date('Due Date')
    repo_id = fields.Many2one('github.repo', string="Github Repository")
    description = fields.Text('Description')

    _sql_constraints = [
         ('milestone_unique', 'unique (repo_id, number)','This milestone existed!')]