# -*- coding: utf-8 -*-
{
    'name': "Helpline Issued",

    'summary': """Custom Helpline Issued""",

    'description': """Custom Helpline Issued for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_membership_member', 'asb_membership', 'asb_master', 'asb_helpline'],
    'data': [
        'security/ir.model.access.csv',
        'views/issued_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
