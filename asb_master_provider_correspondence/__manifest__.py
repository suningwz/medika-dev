# -*- coding: utf-8 -*-
{
    'name': 'Master Configuration Correspondence',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Configuration Correspondence',
    'description': '''
        Custom master configuration correspondence module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_provider', 'asb_master_configuration'],

    'data': [
        'security/ir.model.access.csv',
        'views/master_configuration_correspondence_views.xml',
        'views/master_configuration_correspondence_type_views.xml',
        'reports/report_correspondence_type.xml',
    ],
}
