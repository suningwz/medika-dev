# -*- coding: utf-8 -*-
{
    'name': "Helpline Supporting Ambulance RS",
    'summary': """Custom Helpline Supporting Ambulance RS""",
    'description': """Custom Helpline Supproting Ambulance RS for PT. Medika Plaza""",
    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_membership_member', 'asb_membership', 'asb_master', 'asb_helpline', 'asb_helpline_supporting', 'asb_helpline_call_record'],
    'data': [
        'security/ir.model.access.csv',
        'views/asb_helpline_supporting_ambulance_rs_views.xml',
    ],
}
