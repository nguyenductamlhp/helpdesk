# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

import urllib.request
from urllib.request import urlopen
from github import Github

from odoo import api, fields, models
from odoo.exceptions import Warning


class ProjectTask(models.Model):
    _inherit = 'project.task'

    issue_number = fields.Integer('Issue')
    issue_url = fields.Char(
        'Issue URL',
        compute='compute_issue_url',
        store=True
    )
    milestone_id = fields.Many2one(
        'project.milestone', 'Milestone',
        domain="[('project_id','=', project_id)]")

    _sql_constraints = [
         ('issue_number', 'unique (issue_url)','This issue existed!')]

    @api.depends('issue_number', 'project_id')
    @api.multi
    def compute_issue_url(self):
        """
        """
        url = 'https://github.com/%s/%s/issues/%s'
        for rec in self:
            if not rec.project_id:
                continue
            if not rec.issue_number:
                continue
            owner = rec.project_id.repo_owner_id
            if not owner:
                continue
            login = owner.github_login
            repository = rec.project_id.repository
            issue_number = rec.issue_number

            if all([login, repository, issue_number]):
                rec.issue_url = url % (
                    login, repository, issue_number)

    @api.multi
    def is_issue_exist(self):
        """
        Return True if issue does not exist on github, else False
        """
        self.ensure_one()
        project = self.project_id
        owner = project and project.repo_owner_id or None
        if not project or not owner:
            return False

        login = owner.github_login
        password = owner.github_password
        repository = project.repository

        github = Github(login, password)
        repo = github.get_repo('%s/%s' % (login, repository))
        exist_numbers = []
        try:
            open_issues = repo.get_issues(state='open')
            exist_numbers.extend([issue.number for issue in open_issues])
        except:
            pass
        try:
            close_issues = repo.get_issues(state='close')
            exist_numbers.extend([issue.number for issue in close_issues])
        except:
            pass
        if self.issue_number not in exist_numbers:
            return False
        return True

    @api.multi
    def check_issue_exist(self):
        for rec in self:
            if not rec.is_issue_exist():
                raise Warning('Issue does not exist!')
            else:
                raise Warning('This Issue existed!')

    @api.multi
    def pull_issue_info(self):
        for rec in self:
            if not rec.is_issue_exist():
                raise Warning('Issue does not exist!')
            project = rec.project_id or None
            owner = project and project.repo_owner_id or None
            if not project or not owner:
                raise Warning('No project on task!')

            login = owner.github_login
            password = owner.github_password
            repository = project.repository

            github = Github(login, password)
            repo = github.get_repo('%s/%s' % (login, repository))
            issue= repo.get_issue(rec.issue_number)
            rec.name= issue.title
            rec.description = issue.body

    @api.multi
    def push_issue_info(self):
        for rec in self:
            if not rec.is_issue_exist():
                raise Warning('Issue does not exist!')
            project = rec.project_id or None
            owner = project and project.repo_owner_id or None
            if not project or not owner:
                raise Warning('No project on task!')

            login = owner.github_login
            password = owner.github_password
            repository = project.repository

            github = Github(login, password)
            repo = github.get_repo('%s/%s' % (login, repository))
            issue= repo.get_issue(rec.issue_number)
            issue.edit(title=rec.name, body=rec.description)

    @api.multi
    def merge_issue_info(self):
        for rec in self:
            if not rec.is_issue_exist():
                raise Warning('Issue does not exist!')
            project = rec.project_id or None
            owner = project and project.repo_owner_id or None
            if not project or not owner:
                raise Warning('No project on task!')

            login = owner.github_login
            password = owner.github_password
            repository = project.repository

            github = Github(login, password)
            repo = github.get_repo('%s/%s' % (login, repository))
            issue = repo.get_issue(rec.issue_number)
            # Merge field
            title = issue.title + '\n' + rec.name
            description = issue.body + '\n' + rec.description
            # Set back to both issue and tasks
            issue.edit(title=title, body=description)
            rec.name = title
            rec.description = description

    @api.multi
    def create_issue(self):
        """
        Create issue on github from currnt task
        """
        for rec in self:
            if rec.issue_number:
                raise Warning('Task already has issue!')
            project = rec.project_id or None
            owner = project and project.repo_owner_id or None
            if not project or not owner:
                raise Warning('No project on task!')

            login = owner.github_login
            password = owner.github_password
            repository = project.repository

            github = Github(login, password)
            repo = github.get_repo('%s/%s' % (login, repository))
            issue = repo.create_issue(
                rec.name,
                body=rec.description)
            rec.issue_number = issue.number
