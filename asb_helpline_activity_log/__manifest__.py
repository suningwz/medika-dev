# -*- coding: utf-8 -*-
{
    'name': "Helpline Activity Log",

    'summary': """Custom Helpline Activity Log""",

    'description': """Custom Helpline Activity Log for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_helpline'],
    'data': [
        'security/ir.model.access.csv',
        'views/activity_log_views.xml',
        # 'views/guarantee_letter_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
