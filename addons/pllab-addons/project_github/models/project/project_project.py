# -*- encoding: utf-8 -*-
###############################################################################
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>               #
###############################################################################

import urllib.request
from urllib.request import urlopen
from github import Github

from odoo import api, fields, models
from odoo.exceptions import Warning


class ProjectProject(models.Model):
    _inherit = 'project.project'

    repo_id = fields.Many2one(
        'github.repo', 'Repository')
    repository = fields.Char(
        'Repository')
    repo_owner_id = fields.Many2one(
        'res.partner', 'Repository Owner')
    milestone_ids = fields.One2many(
        'project.milestone', 'project_id', string="Milestones")

    @api.multi
    def pull_repo_milestone(self):
        """
        Sync milestone from github to project milestone
        """
        milestone_env = self.env['project.milestone']
        for rec in self:
            if not all([rec.repo_owner_id, rec.repo_owner_id]):
                continue
            login = rec.repo_owner_id.github_login
            password = rec.repo_owner_id.github_password
            if not all([login, password]):
                raise Warning('Setup github on repository onwer!')
            github = Github(login, password)
            g_repo = github.get_repo('%s/%s' % (login, rec.repository))
            # Get open milestone
            open_milestones = g_repo.get_milestones(state='open')
            for milestone in open_milestones:
                # If milestone exist, update
                number = milestone.number
                milestones = milestone_env.search(
                    [
                        ('project_id', '=', rec.id),
                        ('number', '=', int(number)),
                    ])
                if milestones:
                    vals = {
                        'state': milestone.state,
                        'description': milestone.description,
                        'name': milestone.title,
                        'due_date': milestone.due_on
                    }
                    milestones.write(vals)
                else:
                    vals = {
                        'project_id': rec.id,
                        'state': 'open',
                        'description': milestone.description,
                        'name': milestone.title,
                        'number': milestone.number,
                        'due_date': milestone.due_on
                    }
                    milestone_env.create(vals)
            # Get close milestone
            close_milestones = g_repo.get_milestones(state='close')
            for milestone in close_milestones:
                # If milestone exist, update
                number = milestone.number
                milestones = milestone_env.search(
                    [
                        ('project_id', '=', rec.id),
                        ('number', '=', int(number)),
                    ])
                if milestones:
                    vals = {
                        'state': milestone.state,
                        'description': milestone.description,
                        'name': milestone.title,
                        'due_date': milestone.due_on
                    }
                    milestones.write(vals)
                else:

                    vals = {
                        'project_id': rec.id,
                        'state': 'open',
                        'description': milestone.description,
                        'name': milestone.title,
                        'number': milestone.number,
                        'due_date': milestone.due_on
                    }
                    milestone_env.create(vals)
                    