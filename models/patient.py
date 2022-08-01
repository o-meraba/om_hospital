from odoo import api, fields, models
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string="Name", tracking=True)
    date_of_birth = fields.Date("Date Of Birth")
    age = fields.Integer(string="Age", compute='_compute_age')  # if there is compute feature, it won't be stored in db, if you want, you can add store=True
    ref = fields.Char(string="Reference", default='HB00')
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string='Gender', default='male')
    active = fields.Boolean(string="Active", default=True)
    note = fields.Text(string="Description", tracking=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")

    @api.depends('date_of_birth')  # for compute before clicking save button
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0