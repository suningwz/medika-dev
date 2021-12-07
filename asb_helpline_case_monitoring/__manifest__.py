# -*- coding: utf-8 -*-
{
    'name': "Helpline Case Monitoring",

    'summary': """Custom Helpline Case Monitoring""",

    'description': """Custom Helpline Case Monitoring for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'mail','portal', 'asb_membership_member','asb_membership_client', 'asb_membership', 'asb_master', 'asb_helpline', 'asb_helpline_guarantee_letter', 'asb_master_diagnosis'],
    'data': [
        'security/ir.model.access.csv',
        'views/case_monitoring_views.xml',
        'views/monitoring_detail_remarks_views.xml',
        'views/guarantee_letter_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
