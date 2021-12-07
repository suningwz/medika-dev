# -*- coding: utf-8 -*-
{
    'name': "Membership",

    'summary': """
        Custom Membership""",

    'description': """
        Custom Membership for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail', 'portal'],
    'data': [
        'security/membership_security.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
}
