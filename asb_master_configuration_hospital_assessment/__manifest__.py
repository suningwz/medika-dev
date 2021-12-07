# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Hospital Assessment',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Hospital Assessment',
    'description': '''
        Custom master configuration hospital assessment module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration', 'asb_master_configuration_facility_category'],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_hospital_assessment_views.xml',
    ],
}