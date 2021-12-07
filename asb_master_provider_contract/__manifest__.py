# -*- coding: utf-8 -*-
{
    'name': 'Master Provider Contract',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Provider Contract',
    'description': '''
        Custom master contract module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_provider', 'asb_binary_newtab'],

    'data': [
        'security/ir.model.access.csv',
        'data/contract_status.xml',
        'views/master_provider_contract_views.xml',
    ],
}
