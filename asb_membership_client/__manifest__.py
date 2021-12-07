# -*- coding: utf-8 -*-
{
    'name': "Membership Client",

    'summary': """
        Custom Membership Client""",

    'description': """
        Custom Membership Client for PT. Medika Plaza
    """,

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'web', 'asb_master', 'mail', 'portal', 'product', 'asb_state_city', 'asb_membership',  'asb_master_diagnosis', 'asb_master_provider'],
    'data': [
        'security/ir.model.access.csv',
        'views/client_branch_views.xml',
        'views/assets.xml',
        'views/client_views.xml',
        'views/client_activity_views.xml',
        'views/client_program_views.xml',
        'views/client_program_plan_views.xml',
        'views/client_program_floatfund_views.xml',
        'views/client_program_plan_header_views.xml',
        'views/header_detail_views.xml',
    ],
    'installable': True,
    'application': True,
}
