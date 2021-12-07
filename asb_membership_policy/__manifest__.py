# -*- coding: utf-8 -*-
{
    'name': "Membership Policy",

    'summary': """
        Custom Membership Policy""",

    'description': """
        Custom Membership Policy for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_master', 'asb_membership', 'asb_membership_client', 'asb_membership_member', 'mail', 'portal', 'product', 'contacts_maps'],
    'data': [
        'security/ir.model.access.csv',
        'data/policy_status.xml',
        'wizard/policy_member_views.xml',
        'views/policy_views.xml',
        'views/client_views.xml',
    ],
    'installable': True,
    'application': True,
}
