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

    name = fields.Char(string="Name", tracking=True)  #name field created
    date_of_birth = fields.Date("Date Of Birth")
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age', tracking=True)  # if there is compute feature, it won't be stored in db, if you want, you can add store=True
    ref = fields.Char(string="Reference")
    gender = fields.Selection([('male', "Male"), ('female', 'Female')], string='Gender', default='male')
    active = fields.Boolean(string="Active", default=True)
    note = fields.Text(string="Description", tracking=True)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointments')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")


    second_language = fields.Char(string="Second Language")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])


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


    def action_test(self):
        print("Clicked Action TEST")
        return


    def get_second_l(self):

        second_language_data_2 = self.env['ir.translation'].search(
            [('name', '=', 'product.template,name'),
             ('res_id', '=', self.env['product.template'].search([('id', '=', self.id)]).id),
             ('lang', '=', 'en_US')]).value
        print(second_language_data_2)