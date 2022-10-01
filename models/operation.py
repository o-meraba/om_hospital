from odoo import api, fields, models

class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    _log_access = False # Remove create_date, create_uid, write_date, write_uid columns

    doctor_id = fields.Many2one('res.users', string='Doctor')
