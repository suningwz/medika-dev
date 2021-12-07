# -*- coding: utf-8 -*-
{
    'name': "Membership Client Terms and Conditions",

    'summary': """
        Custom Membership Client Terms and Conditions""",

    'description': """
        Custom Membership Client Terms and Conditions for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_membership_client', 'asb_helpline_call_record', 'asb_binary_newtab'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/client_views.xml',
    ],
    'installable': True,
    'application': True,
}
