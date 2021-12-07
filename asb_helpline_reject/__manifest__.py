# -*- coding: utf-8 -*-
{
    'name': "Helpline Reject",

    'summary': """Custom Helpline Reject""",

    'description': """Custom Helpline Reject for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_helpline_guarantee_letter'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_reject_reason_views.xml',
        'views/guarantee_letter_views.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
