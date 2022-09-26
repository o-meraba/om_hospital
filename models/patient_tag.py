from odoo import api, fields, models


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = self.name + " (Copy)"
            default['sequence'] = self.sequence + 100

        return super(PatientTag, self).copy(default)



    _sql_constraints = [
        ('name_uniq', 'unique (name, active)', 'Tag name must be unique'),
        ('check_sequence', 'CHECK(sequence > 0)', 'Sequence must be bigger than zero'),
        ('seq_uniq', 'unique (sequence)', 'Sequence must be unique'),
    ]

