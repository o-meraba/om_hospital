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
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
    ],
    'demo': [],
    'application': 'True',
    'installable': True,
    'auto_install': False,
    'assets': {},
    'licence': 'LPGL-3',
}
