# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Facility Category',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Facility Category',
    'description': '''
        Custom master configuration facility category module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration',],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_facility_category_views.xml',
    ],
}