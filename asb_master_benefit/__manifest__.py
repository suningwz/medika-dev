# -*- coding: utf-8 -*-
{
    'name': 'Master Benefit',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Benefit',
    'description': '''
        Custom master benefit module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master', 'asb_master_configuration_benefit'],

    'data': [
        'security/ir.model.access.csv',
        'views/master_benefit_views.xml',
    ],
}