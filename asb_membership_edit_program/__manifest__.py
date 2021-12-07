# -*- coding: utf-8 -*-
{
    'name': "Membership Edit Program Plan Header",

    'summary': """
        Custom Membership Edit Program Plan Header""",

    'description': """
        Custom Membership Edit Program Plan Header for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_master', 'mail', 'portal', 'product', 'contacts_maps', 'asb_membership_client', 'asb_membership'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/edit_program_views.xml',
        'wizard/edit_program_plan_views.xml',
    ],
    'installable': True,
    'application': True,
}
