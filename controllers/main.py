from odoo import http
from odoo.http import request

class Hospital(http.Controller):
    @http.route('/hospital/doctor/', website=True, auth='public')
    def hospital_doctor(self, **kw):
        # return "Hello,World"
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("om_hospital.patients_page",{
            'patients': patients,
        })