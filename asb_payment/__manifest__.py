# -*- coding: utf-8 -*-
{
    'name': "Payment",

    'summary': """Custom Payment""",

    'description': """Custom Payment for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/payment_security.xml',
        'views/views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
