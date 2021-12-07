# -*- coding: utf-8 -*-
{
    'name': "Eclaim Productivity",

    'summary': """Custom Eclaim Productivity""",

    'description': """Custom Eclaim Productivity for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_productivity'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/eclaim_user_productivity_views.xml',
        'views/res_users_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
