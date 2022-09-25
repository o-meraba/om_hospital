from odoo import api, fields, models


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ('name_uniq', 'unique (name, active)', 'Tag name must be unique'),
        ('check_sequence', 'CHECK(sequence > 0)', 'Sequence must be bigger than zero'),
        ('seq_uniq', 'unique (sequence)', 'Sequence must be unique'),
    ]