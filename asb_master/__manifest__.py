# -*- coding: utf-8 -*-
{
    'name': 'Master',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master',
    'description': '''
        Custom master module for Medika
    ''',
    'depends': ['base'],

    'data': [
        'views/master_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}