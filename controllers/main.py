from odoo import http
from odoo.http import request
import logging
import werkzeug

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home, SIGN_UP_REQUEST_PARAMS
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request

class Hospital(http.Controller):
    @http.route('/hospital/doctor/', website=True, auth='public')
    def hospital_doctor(self, **kw):
        # return "Hello,World"
        patients = request.env['hospital.patient'].sudo().search([])
        return request.render("om_hospital.patients_page",{
            'patients': patients,
        })

class AuthSignupHome(Home):

    def _prepare_signup_values(self, qcontext):
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
       
        if len(values.get('password')) < 8:
            raise UserError(_('Şifre 8 karakterden kısa. Lütfen yeni bir şifre girin.Hospitalll'))
           
        return values 