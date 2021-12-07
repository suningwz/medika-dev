# -*- coding: utf-8 -*-
{
    'name': 'Master Provider',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Provider',
    'description': '''
        Custom master provider module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master', 'asb_master_configuration_hospital_assessment', 'asb_master_configuration_bank', 'asb_master_configuration_pic_title', 'asb_state_city'],

    'data': [
        'security/ir.model.access.csv',
        'views/master_provider_views.xml',
        'views/tid_information_views.xml',
    ],
}
