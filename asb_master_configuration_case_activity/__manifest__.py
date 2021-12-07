# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Case Activity',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Case Activity',
    'description': '''
        Custom master configuration case activity module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration',],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_case_activity_views.xml',
    ],
}