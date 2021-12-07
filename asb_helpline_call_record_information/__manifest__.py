# -*- coding: utf-8 -*-
{
    'name': "Helpline Call Record Information",

    'summary': """Custom Helpline Call Record Information""",

    'description': """Custom Helpline Call Record Information for PT. Medika Plaza""",

    'author': "PT. Arkana Solusi Bisnis",
    'website': "http://www.arkana.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'asb_helpline_call_record', 'asb_helpline_guarantee_letter', 'asb_master_provider', 'asb_master_benefit', 'asb_klinik_costing_product_information', 'asb_klinik_costing_package', 'asb_helpline_supporting_ambulance_rental', 'asb_helpline_supporting_ambulance_rs', 'asb_helpline_supporting_assistance', 'asb_helpline_supporting_eap', 'asb_helpline_supporting_embassy', 'asb_helpline_supporting_specialist'],
    'data': [
        'security/ir.model.access.csv',
        'views/call_record_views.xml',
        'views/ticketing_information_views.xml',
        'report/information_package_mcu.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
