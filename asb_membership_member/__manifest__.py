# -*- coding: utf-8 -*-
{
    'name': "Membership Member",
    'summary': "Custom Membership Member",
    'description': "Custom Membership Member for PT. Medika Plaza",
    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_master', 'asb_membership', 'asb_membership_client', 'asb_state_city', 'mail', 'portal', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/member_views.xml',
        'views/suffix_id_views.xml',
        'views/plan_information_views.xml',
        'views/member_history_views.xml',
        'views/client_branch_views.xml',
        'data/suffix_id_data.xml',
        'data/employment_status.xml',
        'report/card_member.xml',
        'views/send_card_member_views.xml',
        'data/card_member_email_template.xml'
    ],
}
