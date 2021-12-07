# -*- coding: utf-8 -*-
{
    'name'          :   "Master Poli Perawat Klinik",

    'summary'       :   """
                        Module Master Poli Perawat Klinik
                        """,

    'description'   :   """
                        Module Master Poli Perawat Klinik
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
                            'asb_klinik_master_data_klinik',
                            'asb_klinik_costing',
                            'asb_klinik_admission',
                        ],

    # always loaded
    'data'          :   [
                            'security/admission_poli_perawat_security.xml',
                            'security/ir.model.access.csv',
                            'views/views.xml',
                            'views/master_poli_perawat_view.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}
