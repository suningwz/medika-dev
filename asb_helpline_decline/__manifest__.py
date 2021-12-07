# -*- coding: utf-8 -*-
{
    'name': "Helpline Decline",

    'summary': """Custom Helpline Decline""",

    'description': """Custom Helpline Decline for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal', 'asb_helpline_guarantee_letter'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard_decline_reason_views.xml',
        'views/guarantee_letter_views.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
