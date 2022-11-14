# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Hospital management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Omer ABA',
    'sequence': -100,
    'summary': 'Hospital management system',
    'description': """ Hospital management system """,
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/cancel_appointment_view.xml',
        'data/patient_tag_data.xml',
        'data/sequence_data.xml',
        'data/patient.tag.csv',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_views.xml',
        'views/operation_view.xml',
        'views/odoo_playground_view.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'report/patient_details_template.xml',
    ],
    'demo': [],
    'application': 'True',
    'installable': True,
    'auto_install': False,
    'assets': {},
    'licence': 'LPGL-3',
}
