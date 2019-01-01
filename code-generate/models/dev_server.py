# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _

CONCURENT_USER_PER_WORKER = 6
HEAVY_WORKER_RATIO = 0.2
LIGHT_WORKER_RATIO = 0.8
LIGHT_WORKER_RAM_ESTIMATION = 150
HEAVY_WORKER_RAM_ESTIMATION = 1024
RAM_PER_WORKER = (
    (LIGHT_WORKER_RATIO * LIGHT_WORKER_RAM_ESTIMATION) + \
    (HEAVY_WORKER_RATIO * HEAVY_WORKER_RAM_ESTIMATION))



class Server(models.Model):
    _name = 'dev.server'

    name = fields.Char(
        string='Name', required=True)
    n_core = fields.Integer(
        string='CPU', required=True, help='Number of CPU cores')
    cron_workers = fields.Integer(
        string='Cron Workers', required=True, help='Number of workers for cron',
        default=1)
    server_ram = fields.Float(
        string='Server RAM', required=True, help='RAM')
    propose_ram = fields.Float(
        string='Propose RAM', help='Propos RAM',
        compute='compute_propose_ram')

    concurrent_user = fields.Integer(
        string=' Theorical Concurrent User', required=False,
        help='Estimation of concurrent users',
        compute='compute_number_of_workers')
    workers = fields.Integer(
        string='Workers',
        help='Number of worker(s)',
        compute='compute_number_of_workers')

    def compute_number_of_workers(self):
        for rec in self:
            rec.workers = (rec.n_core * 2 + 1) - rec.cron_workers
            rec.concurrent_user = rec.workers * CONCURENT_USER_PER_WORKER

    def compute_propose_ram(self):
        for rec in self:
            rec.propose_ram = (
                rec.workers + rec.cron_workers) * RAM_PER_WORKER / 1024