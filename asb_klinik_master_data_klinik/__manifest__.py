# -*- coding: utf-8 -*-
{
    'name'          :   "Master Data Klinik",

    'summary'       :   """
                        Module Master Data Klinik
                        """,

    'description'   :   """
                        Module Master Data Klinik
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
                            'base', 
                            'mail', 
                            'asb_klinik_master_cost_allocation',
                            'asb_klinik_master_poli_unit', 
                            'asb_klinik_master_fasilitas_kesehatan', 
                            'asb_klinik_master_ketenagaan',
                            'asb_klinik_master_personil',
                            'asb_klinik_master_product',
                            'asb_membership_client',
                        ],

    # always loaded
    'data'          :   [
                            'security/profile_user_security.xml',
                            'security/ir.model.access.csv',
                            'views/res_users_view.xml',
                            'views/views.xml',
                        ],
    # only loaded in demonstration mode
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}
