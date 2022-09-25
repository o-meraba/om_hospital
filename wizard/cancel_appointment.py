import datetime
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        print("Default get executed", res)
        res['date_cancel'] = datetime.date.today()
        print("Default get executed 2", res)
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    reason = fields.Text(string="Reason", default='Test Reason')
    date_cancel = fields.Date(string="Cancellation Date")


    def action_cancel(self):
        if self.appointment_id.booking_date == fields.Date.today():
            raise ValidationError("Sorry, cancellation is not allow the same day of booking")
        return


