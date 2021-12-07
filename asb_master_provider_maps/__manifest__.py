# -*- coding: utf-8 -*-
{
    'name': 'Master Provider Maps',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Provider Maps',
    'description': '''
        Custom master maps module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_provider', 'contacts_maps'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/master_provider_maps_views.xml',
    ],
}