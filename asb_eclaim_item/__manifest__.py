# -*- coding: utf-8 -*-
{
    'name': "E-Claim Item",

    'summary': """Custom E-Claim Item""",

    'description': """Custom E-Claim Item for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_eclaim', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/item_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
