# -*- coding: utf-8 -*-
{
    'name': 'Master Provider Dashboard',
    'version': '0.1',
    'author': 'PT Arkana Solusi Bisnis',
    'license': 'OPL-1',
    'category': 'Master',
    'website': 'http://www.arkana.co.id',
    'summary': 'Custom Master Provider Dashboard',
    'description': '''
        Custom master Dashboard module for Medika
    ''',
    'depends': ['base', 'mail', 'portal', 'asb_master_provider', 'asb_master_provider_contract', 'asb_master_provider_rebate', 'asb_master_provider_discount'],

    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/master_provider_views.xml',
        'views/menu_dashboard_qweb_views.xml',
    ],
    'qweb': [
        'static/src/xml/master_provider_dashboard_template.xml',
    ],
}
