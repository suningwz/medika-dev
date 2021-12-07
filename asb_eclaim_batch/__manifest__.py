# -*- coding: utf-8 -*-
{
    'name': "E-Claim Batch ",

    'summary': """Custom E-Claim Batch""",

    'description': """Custom E-Claim Batch for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_eclaim', 'asb_eclaim_eclaim', 'asb_helpline_guarantee_letter', 'mail', 'portal'],
    'data': [
        'security/ir.model.access.csv',
        'data/batch_due_date.xml',
        'views/batch_views.xml',
        # 'views/invoice_detail_views.xml',
        'views/guarantee_letter_views.xml',
        'views/search_guarantee_letter_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
