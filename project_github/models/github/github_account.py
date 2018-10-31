# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from github import Github

from odoo import models, fields, api


class GithubAccount(models.Model):
    _name = 'github.account'

    name = fields.Char('Name', compute='get_name')
    login = fields.Char('Username', size=100, required=True)
    password = fields.Char('Password', size=100, required=True)

    partner_id = fields.Many2one('res.partner', string="Partner")
    repo_ids = fields.One2many(
        'github.repo', 'account_id', string='Repositories')

    @api.depends('login', 'password')
    def get_name(self):
        for rec in self:
            if all([rec.login, rec.password]):
                github = Github(rec.login, rec.password)
                rec.name = github.get_user().name

    @api.multi
    def get_repositories(self):
        self.ensure_one()
        repo_env = self.env['github.repo']
        github = Github(self.login, self.password)
        repos = list(github.get_user().get_repos())
        for repo in repos:
            fullname = repo.full_name
            if fullname:
                info = fullname.split('/')
                # TODO: pull repo of other acc but joined
                if self.login != info[0]:
                    continue
                exist_repo = repo_env.search(
                    [
                        ('account_id', '=', self.id),
                        ('name', '=', info[1])
                    ]
                )
                if exist_repo:
                    continue
                vals = {
                    'name': info[1],
                    'account_id': self.id
                }
                repo_env.create(vals)
