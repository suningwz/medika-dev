# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration PIC Title',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration PIC Title',
    'description': '''
        Custom master configuration PIC Title module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_configuration'],

    'data': [
        'security/ir.model.access.csv',
        'views/pic_title_views.xml',
    ],
}
