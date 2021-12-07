# -*- coding: utf-8 -*-
{
    'name'          :   "Master Reservation Klinik",

    'summary'       :   """
                        Module Master Reservation Klinik
                        """,

    'description'   :   """
                        Module Master Reservation Klinik
                        """,

    'author'        :   "PT. Arkana Solusi Bisnis",
    'website'       :   "https://arkana.co.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category'      :   'Uncategorized',
    'version'       :   '0.1',

    # any module necessary for this one to work correctly
    'depends'       :   [
                            'web',
                            'base', 
                            'mail', 
                            'product',
                            'asb_klinik_master_cost_allocation',
                            'asb_klinik_master_poli_unit',
                            'asb_klinik_master_fasilitas_kesehatan',
                            'asb_klinik_master_ketenagaan',
                            'asb_klinik_master_personil',
                            'asb_klinik_master_product',
                            'asb_klinik_costing_package',
                            'asb_klinik_costing_setting_general',
                            'asb_klinik_costing_setting_onsite',
                            'asb_klinik_admission_team',
                        ],

    # always loaded
    'data'          :   [
                            'security/admission_reservation_security.xml',
                            'security/ir.model.access.csv',
                            'data/master_reservation_data.xml',
                            'views/assets.xml',
                            'views/master_reservation_view.xml',
                        ],
    'qweb'          :   [
                            'static/src/xml/master_reservation_dashboard_template.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
