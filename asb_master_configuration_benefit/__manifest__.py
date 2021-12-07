# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Benefit',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Benefit',
    'description': '''
        Custom master configuration benefit module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration', ],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_benefit_views.xml',
        'views/master_configuration_edc_views.xml',
    ],
}
