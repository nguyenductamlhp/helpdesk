# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import api, fields, models
from odoo.exceptions import Warning

TAB = '    '

DEFAULT_HEADER = '''
# -*- encoding: utf-8 -*-
# Copyright (C) 2018 Nguyen Duc Tam <nguyenductamlhp@gmail.com>

from odoo import fields, models, api, _
'''
CLASS_DEFINE = 'class %s(models.%s):\n'
LIST_VIEW = '''
<record id="view_%s_tree" model="ir.ui.view">
    <field name="name">view.%s.tree</field>
    <field name="model">%s</field>
    <field name="arch" type="xml">
        <tree>
%s
        </tree>
    </field>
</record>
'''
FORM_VIEW = '''
<record id="view_%s_form" model="ir.ui.view">
    <field name="name">view.%s.form</field>
    <field name="model">%s</field>
    <field name="arch" type="xml">
        <form>
            <header>
            </header>
            <sheet>
                <div class="oe_title">
                </div>
                <group>
                    <group string="Group 1">
%s
                    </group>
                    <group string="Group 2">
                    </group>
                </group>
                <notebook>
                    <page string="Page 1">
                    </page>
                    <page string="Page 2">
                    </page>
                </notebook>
            </sheet>
        </form>
    </field>
</record>
'''
ACTION = '''
<record id="action_%s" model="ir.actions.act_window">
    <field name="name">action.%s</field>
    <field name="type">ir.actions.act_window</field>
    <field name="res_model">%s</field>
    <field name="view_type">form</field>
    <field name="view_mode">tree,form,kanban</field>
</record>
'''
MENU = '''
<menuitem id="menu_%s_view"
    name="%s"
    action="action_%s"
    sequence="10"
    parent=""
    groups="base.group_user"/>
'''


class CodeModel(models.Model):
    _name = 'code.model'
    _rec_name = 'model_string'

    model_string = fields.Char('Model Name', required=True)
    model_name = fields.Char(
        'Technical Name',
        compute='compute_model_name',
        inverse='inverse_model_name', store=True)
    is_inherit = fields.Boolean('Is Inherit?')
    model_type = fields.Selection(
        [
            ('trainsient', 'TrainsientModel'),
            ('model', 'Model'),
            ('abstract', 'AbstractModel')
        ],
        default='model',
        string='Model Type'
    )
    field_ids = fields.One2many(
        'code.field', 'model_id', string="Fields")
    note = fields.Text('Note')


    model_define = fields.Text(
        compute='generate_model_define',
        # inverse='inverse_model_define',
        string='Model Definition')
    list_view_define = fields.Text(
        compute='generate_list_view_define',
        string='List View Definition')
    form_view_define = fields.Text(
        compute='generate_form_view_define',
        string='Form View Definition')
    menu_action_define = fields.Text(
        compute='generate_menu_action_define',
        string='Menu Action Definition')


    @api.depends('model_string')
    def compute_model_name(self):
        for model in self:
            if model.model_name:
                continue
            string = model.model_string or None
            if not string:
                continue
            arr = string.split(' ')
            model.model_name = ('.'.join(arr)).lower()

    def inverse_model_name(self):
        for rec in self:
            name = rec.model_name

    def generate_model_define(self):
        for model in self:
            result = DEFAULT_HEADER + 2 * '\n'

            class_name = model.model_string.replace(' ', '')
            model_type = dict(self._fields[
                'model_type'].selection).get(model.model_type)
            class_line = CLASS_DEFINE % (
                class_name, model_type)
            result += class_line

            define_line = TAB + "%s = '%s'\n"
            def_mode = model.is_inherit and '_inherit' or '_name'
            result += define_line % (def_mode, model.model_name)

            for field in  model.field_ids:
                f_code = '\n%s%s' % (TAB, field.python_definition)
                result += f_code

            model.model_define = result

    def generate_list_view_define(self):
        for rec in self:
            list_id = rec.model_name and rec.model_name.replace('.', '_')
            list_name = rec.model_name
            list_model = rec.model_name
            list_body = ''
            for f in rec.field_ids:
                list_body += 3 * TAB + '%s\n' % f.xml_definition
            rec.list_view_define = LIST_VIEW % (
                list_id, list_name, list_model, list_body[:-1])

    def generate_form_view_define(self):
        for rec in self:
            form_id = rec.model_name and rec.model_name.replace('.', '_')
            form_name = rec.model_name
            form_model = rec.model_name
            form_body = ''
            for f in rec.field_ids:
                form_body += 6 * TAB + '%s\n' % f.xml_definition
            rec.form_view_define = FORM_VIEW % (
                form_id, form_name, form_model, form_body[:-1])

    def generate_menu_action_define(self):
        for rec in self:

            action_id = rec.model_name and rec.model_name.replace('.', '_')
            action_name = rec.model_name
            action_model = rec.model_name
            action = ACTION % (
                action_id, action_name, action_model)

            menu_id = rec.model_name and rec.model_name.replace('.', '_')
            menu_name = rec.model_string
            menu_action = rec.model_name and rec.model_name.replace('.', '_')
            menu = MENU % (
                menu_id, menu_name, menu_action)

            rec.menu_action_define = '%s\n%s' % (action, menu)
