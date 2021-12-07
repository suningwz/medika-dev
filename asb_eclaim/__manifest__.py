# -*- coding: utf-8 -*-
{
    'name': "E-Claim",

    'summary': """Custom E-Claim""",

    'description': """Custom E-Claim for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/eclaim_security.xml',
        'views/views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
