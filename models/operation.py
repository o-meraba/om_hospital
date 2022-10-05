from odoo import api, fields, models

class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False # Remove create_date, create_uid, write_date, write_uid columns
    _order = 'sequence,id'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string="Operation Name")
    reference_record = fields.Reference(selection=[('hospital.patient', 'Patient'),
                                                   ('hospital.appointment', 'Appointment')], string='Record')

    sequence = fields.Integer(string="Sequence", default=10)

    @api.model
    def name_create(self, name):
        return self.create({'operation_name': name}).name_get()[0]
