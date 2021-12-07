# -*- coding: utf-8 -*-
{
    'name': "E-Claim Document",

    'summary': """Custom E-Claim Document""",

    'description': """Custom E-Claim Document for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_eclaim', 'asb_eclaim_item', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'views/document_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
