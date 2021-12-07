# -*- coding: utf-8 -*-
{
    'name': 'Master Provider Rebate',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Provider Rebate',
    'description': '''
        Custom master rebate module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_provider', 'asb_master_benefit'],

    'data': [
        'security/ir.model.access.csv',
        'views/master_provider_rebate_views.xml',
    ],
}
