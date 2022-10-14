from locale import currency
import string
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):

    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = "appointment_ref"
    _order = 'id desc'

    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", ondelete='cascade') # you can use just 'hospital.patient' but it should place first in parentheses
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.today)
    gender = fields.Selection(related='patient_id.gender')
    ref = fields.Char(string="Reference", help="Reference of the patient from patient record")
    appointment_ref = fields.Char(string="Appointment Reference")
    prescription = fields.Html(string='Prescription')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel')],default='draft', string="Status", required=True , tracking=True)
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    operation = fields.Many2one('hospital.operation', string='Operation')
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related="company_id.currency_id")
    url = fields.Char(string='URL')
    amount_total = fields.Monetary(string='Total', compute='_compute_amount_total', currency_field='currency_id')

    @api.constrains('booking_date')
    def _check_booking_date(self):
        for rec in self:
            if rec.booking_date and rec.booking_date < fields.Date.today():
                raise ValidationError('The booking date cannot be before today')


    @api.model
    def create(self, vals):
        vals['appointment_ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['appointment_ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).write(vals)


    def _compute_amount_total(self):
        pass
    
    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': "Done",
                'type': 'rainbow_man',
            }
        }    

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_test(self):
       #url action
       return {
           'type' : 'ir.actions.act_url',
           'target' : 'new', # 'target' : 'self',
           'url': self.url  #'url' : 'https://www.odoo.com' , 'http://localhost:8069/shop'
       }

    def action_button(self):
        print("Action button was clicked")
        
    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError('There is no a phone number')
        msg = "Hi %s, your *appointment* number is: %s" % (self.patient_id.name, self.ref)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone, msg)
        return {
           'type': 'ir.actions.act_url',
           'target': 'new',
           'url': whatsapp_api_url
        }
    
    def action_test1(self):
         return {
           'type' : 'ir.actions.act_url',
           'target' : 'new', # 'target' : 'self',
           'url': self.url  #'url' : 'https://www.odoo.com' , 'http://localhost:8069/shop'
        }

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError("The appointment's state is not draft! You can not delete it")
        super(HospitalAppointment, self).unlink()

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = 25
            elif rec.state == 'in_consultation':
                progress = 50
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress
        return

class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(related='product_id.list_price')
    qty = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    price_subtotal = fields.Monetary(string='Subtotal', compute='_compute_price_subtotal', currency_field='companyt_currency_id')
    companyt_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    
    @api.depends('price_unit', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price_unit * rec.qty