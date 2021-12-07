# -*- coding: utf-8 -*-
{
    'name': 'Master Diagnosis',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Diagnosis',
    'description': '''
        Custom master diagnosis module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master',],

    'data': [
        'security/ir.model.access.csv',
        'views/master_diagnosis_views.xml',
    ],
}