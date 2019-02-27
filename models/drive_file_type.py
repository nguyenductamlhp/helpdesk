# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class DriveFileType(models.Model):
    _description = 'Drive Category'
    _name = 'drive.file.type'

    name = fields.Char("Type Name", required=True)
    code = fields.Char("Code", required=True)
    description = fields.Text("Description")
    is_dir = fields.Boolean("Is Directory", default=False)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Code must be unique!')
    ]

    @api.model
    def get_file_type(self, code):
        """
        Return file tye records if exist. Else create new and return
        """
        if not code:
            return None
        file_type = self.search([('code', '=', code)], limit=1)
        if not file_type:
            file_type = self.create({
                'name': code,
                'code': code,
            })
        return file_type
