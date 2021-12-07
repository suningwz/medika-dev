# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Remarks',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Remarks',
    'description': '''
        Custom master configuration remarks module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration',],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_remarks_views.xml',
    ],
}