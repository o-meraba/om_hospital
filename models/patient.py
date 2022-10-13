import datetime

from odoo import api, fields, models
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string="Name", tracking=True)  #name field created & tracking=True (=100)
    date_of_birth = fields.Date("Date Of Birth", tracking=30)
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age',
                         search='_search_age', tracking=20)  # if there is compute feature, it won't be stored in db, if you want, you can add store=True
    ref = fields.Char(string="Reference",tracking=10)
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string='Gender', default='male')
    active = fields.Boolean(string="Active", default=True, tracking=40)
    note = fields.Text(string="Description", tracking=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments', tracking=80)
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags", tracking=60)
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday')
    phone = fields.Char(string="Phone", tracking=120)
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    second_language = fields.Char(string="Second Language")

    def action_view_appointment(self):
        return {
            'name': ('Appointments'),
            'view_mode': 'tree,form',
            'res_model': 'hospital.appointment',
            'type': 'ir.actions.act_window',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
        }

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
            appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'],
                                                                                       groupby=['patient_id'])
            for appointment in appointment_group:
                patient_id = appointment.get('patient_id')[0]
                patient_rec = self.browse(patient_id)
                patient_rec.appointment_count = appointment['patient_id_count']
                self -= patient_rec
            self.appointment_count = 0


    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError('The date of birth cannot be after today')

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError("you can not delete a patient which has appointment!")

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and  not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')  # for compute before clicking save button
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):  # this function is for searchable non stored compute field
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]


    def action_test(self):
        print("Clicked Action TEST")
        return
    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday
    def get_second_l(self):

        second_language_data_2 = self.env['ir.translation'].search(
            [('name', '=', 'product.template,name'),
             ('res_id', '=', self.env['product.template'].search([('id', '=', self.id)]).id),
             ('lang', '=', 'en_US')]).value
        print(second_language_data_2)