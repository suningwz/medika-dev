# -*- coding: utf-8 -*-
{
    'name': "E-Claim Finance Batch",

    'summary': """Custom E-Claim Finance Batch""",

    'description': """Custom E-Claim Finance Batch for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_eclaim', 'asb_eclaim_batch'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/finance_due_date.xml',
        'views/assets.xml',
        'views/batch_views.xml',
    ],
    'qweb': [
        'static/src/xml/eclaim_finance_dashboard_template.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
