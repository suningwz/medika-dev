# -*- coding: utf-8 -*-
{
    'name': "Helpline",

    'summary': """Custom Helpline""",

    'description': """Custom Helpline for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/helpline_security.xml',
        'views/views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
