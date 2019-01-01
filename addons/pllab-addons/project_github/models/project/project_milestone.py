# -*- encoding: utf-8 -*-
###############################################################################
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>               #
###############################################################################

import urllib.request
from urllib.request import urlopen
from datetime import datetime
from github import Github

from odoo import api, fields, models
from odoo.exceptions import Warning


class ProjectMilestone(models.Model):
    _name = 'project.milestone'
    _order = 'name DESC'

    name = fields.Char('Milestone', required=True)
    number = fields.Integer('Number', required=True, default=0)
    milestone_url = fields.Char(
        'Milestone Url', compute='compute_milestone_url')
    project_id = fields.Many2one(
        'project.project', 'Project', required=True)
    description = fields.Text('Description')
    due_date = fields.Date('Due Date')
    state = fields.Selection(
        [
            ('open', 'Open'),
            ('close', 'Close')
        ]
    )

    @api.constrains('name', 'project_id', 'number')
    def constrains_unique_milestone_each_project(self):
        """
        In a project, milestone's name and nuber are unique
        """
        milestone_env = self.env['project.milestone']
        for milestone in self:
            milestones = milestone_env.search(
                [
                    ('id', '!=', milestone.id),
                    ('project_id', '=', milestone.project_id.id),
                    '|', ('name', '=', milestone.name),
                    ('number', '=', milestone.number),
                ])
            if milestones:
                raise Warning('This milestone already existed!')


    def compute_milestone_url(self):
        url = 'https://github.com/%s/%s/milestone/%s'
        for rec in self:
            if not rec.project_id:
                continue
            if not rec.number:
                continue
            owner = rec.project_id.repo_owner_id
            if not owner:
                continue
            login = owner.github_login
            repository = rec.project_id.repository
            number = rec.number

            if all([login, repository, number]):
                rec.milestone_url = url % (
                    login, repository, number)

    @api.multi
    def get_authentic_github_repo(self):
        """
        Return github authentic repository, else False
        """
        self.ensure_one()
        project = self.project_id or None
        if not project:
            raise Warning('No project on milestone!')
        if not all([project.repo_owner_id, project.repo_owner_id]):
            raise Warning('No repository is  set on project!')
        login = project.repo_owner_id.github_login
        password = project.repo_owner_id.github_password
        if not all([login, password]):
            raise Warning('Setup github on repository onwer!')
        github = Github(login, password)
        g_repo = github.get_repo('%s/%s' % (login, project.repository))
        return g_repo or False

    @api.multi
    def is_exist_on_github(self):
        """
        Return True if milestone existed on github, else False
        """
        git_repo = self.get_authentic_github_repo()
        if not git_repo:
            return False

        milestone_names = []
        # Get open milestone
        open_milestones = git_repo.get_milestones(state='open')
        for milestone in open_milestones:
            milestone_names.append(milestone.title)
        # Get close milestone
        close_milestones = git_repo.get_milestones(state='close')
        for milestone in close_milestones:
            milestone_names.append(milestone.title)

        if self.name in milestone_names:
            return True
        return False

    @api.multi
    def push_milestone_info(self):
        """
        Update milestone info to github
        """
        for milestone in self:
            if not milestone.is_exist_on_github():
                milestone.btn_create_git_milestone()

            
            git_repo = milestone.get_authentic_github_repo()
            due_on = milestone.due_date and datetime.strptime(milestone.due_date, '%Y-%m-%d') or None
            git_milestone = git_repo.create_milestone(
                milestone.name,
                state='open',
                description=milestone.description)
            milestone.number = git_milestone.number


    @api.multi
    def btn_create_git_milestone(self):
        """
        Create github milestone
        """
        for milestone in self:
            if milestone.is_exist_on_github():
                raise Warning('This milestone already existed on github!')

            git_repo = milestone.get_authentic_github_repo()
            due_on = milestone.due_date and datetime.strptime(milestone.due_date, '%Y-%m-%d') or None
            git_milestone = git_repo.create_milestone(
                milestone.name,
                state='open',
                description=milestone.description)
            milestone.number = git_milestone.number

    @api.model
    def create(self, vals):
        res = super(ProjectMilestone, self).create(vals)
        res.btn_create_git_milestone()
        return res
