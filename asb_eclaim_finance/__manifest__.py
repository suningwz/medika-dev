# -*- coding: utf-8 -*-
{
    'name': "E-Claim Finance",

    'summary': """Custom E-Claim Finance""",

    'description': """Custom E-Claim Finance for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_eclaim', 'asb_eclaim_batch', 'asb_helpline_guarantee_letter'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/finance_views.xml',
    ],
    'qweb': [
        'static/src/xml/eclaim_finance_dashboard_template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
