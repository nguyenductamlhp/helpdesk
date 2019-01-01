# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import api, fields, models
from odoo.exceptions import Warning

FIELD_PYTHON_PATTERN = "%s = fields.%s(string='%s', required=%s, readonly=%s, help='%s')"
FIELD_XML_PATTERN = '<field name="%s" string="%s"/>'


class CodeField(models.Model):
    _name = 'code.field'
    _rec_name = 'field_string'

    field_string = fields.Char('Field Name', required=True)
    field_name = fields.Char(
        'Technical Name',
        compute='compute_field_name',
        inverse='inverse_field_name',
        store=True)
    is_required = fields.Boolean('Required?')
    is_readonly = fields.Boolean('Readonly?')
    field_type = fields.Selection(
        [
            ('char', 'Char'),
            ('float', 'Float'),
            ('boolean', 'Boolean'),
            ('integer', 'Integer'),
            ('text', 'Text'),
            ('binary', 'Binary'),
            ('many2one', 'Many2one'),
            ('many2many', 'Many2many'),
            ('one2many', 'One2many'),
            ('date', 'Date'),
            ('datetime', 'DateTime'),
            ('selection', 'Selection'),
         ],
        required=True,
        default='char',
        string='Model Type'
    )
    field_help = fields.Text('Help', default='')
    model_id = fields.Many2one(
        'code.model', string='Model')

    python_definition = fields.Text(
        compute='generate_python_definition',
        string='Field Python Definition')
    xml_definition = fields.Text(
        compute='generate_xml_definition',
        string='Field XML Definition')

    @api.depends('field_string')
    def compute_field_name(self):
        for field in self:
            if field.field_name:
                continue
            string = field.field_string or None
            if not string:
                continue
            arr = string.split(' ')
            field.field_name = ('_'.join(arr)).lower()

    def inverse_field_name(self):
        for rec in self:
            continue

    @api.multi
    def generate_python_definition(self):
        for field in self:
            fieldtype = dict(self._fields[
                'field_type'].selection).get(field.field_type)
            field.python_definition = FIELD_PYTHON_PATTERN % (
                field.field_name, fieldtype, field.field_string,
                field.is_required, field.is_readonly, field.field_help or field.field_string)

    @api.multi
    def generate_xml_definition(self):
        for field in self:
            field.xml_definition = FIELD_XML_PATTERN % (
                field.field_name, field.field_string)
