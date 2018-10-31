# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import models, fields, api
from github import Github


class GithubRepo(models.Model):
    _name = 'github.repo'

    name = fields.Char('Name', required=True)
    url = fields.Char('URL', compute='compute_repo_url', store=True)

    account_id = fields.Many2one('github.account', string="Github Account")
    partner_id = fields.Many2one(
        'res.partner', related='account_id.partner_id', readonly=True)
    milstone_ids = fields.One2many(
        'github.milestone', 'repo_id', string="Milestones", readonly=True)

    _sql_constraints = [
         ('repo_url_unique', 'unique (url)','This repo existed!')]

    @api.depends('name', 'account_id')
    def compute_repo_url(self):
        for rec in self:
            if all([rec.name, rec.account_id]):
                rec.url = 'http://github.com/%s/%s' % (
                    rec.account_id.login, rec.name)

    @api.multi
    def pull_milestone(self):
        """
        Pull milstone from remote. Update if have change or create if not exist
        """
        milestone_env = self.env['github.milestone']
        for rec in self:
            acc = rec.account_id
            if not acc:
                continue
            github = Github(acc.login, acc.password)
            repo = github.get_repo('%s/%s' % (acc.login, rec.name))
            # Get milestone
            git_milestones = repo.get_milestones()
            for milestone in git_milestones:
                print("milestone", milestone)
                # If milestone exist, update
                print(milestone.number)
                number = milestone.number
                milestones = milestone_env.search(
                    [
                        ('repo_id', '=', rec.id),
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
                        'repo_id': rec.id,
                        'state': 'open',
                        'description': milestone.description,
                        'name': milestone.title,
                        'number': milestone.number,
                        'due_date': milestone.due_on
                    }
                    milestone_env.create(vals)
