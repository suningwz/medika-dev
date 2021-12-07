# -*- coding: utf-8 -*-
{
    'name': "E-Claim Case Monitoring",

    'summary': """Custom E-Claim Case Monitoring""",

    'description': """Custom E-Claim Case Monitoring for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_eclaim', 'asb_eclaim_batch', 'asb_helpline_guarantee_letter', 'mail', 'portal'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/guarantee_letter_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
