# -*- coding: utf-8 -*-
{
    'name': "Helpline Costing Product Information",

    'summary': """Custom Helpline Costing Product Information""",

    'description': """Custom Helpline Costing Product Information for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_klinik_costing'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_information_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
