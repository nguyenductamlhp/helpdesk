# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class DriveTag(models.Model):
    _description = 'Drive Tag'
    _name = 'drive.tag'

    name = fields.Char("Tag Name", required=True)
    description = fields.Text("Description")
    file_ids = fields.Many2many(
        'drive.file', 'file_tag_rel', 'tag_id', 'file_id', string="Files")
