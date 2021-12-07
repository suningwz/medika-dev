# -*- coding: utf-8 -*-
{
    'name'          :   "Master Admission Klinik",

    'summary'       :   """
                        Module Master Admission Klinik
                        """,

    'description'   :   """
                        Module Master Admission Klinik
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
                            'asb_klinik_admission_team',
                            'asb_klinik_admission_reservation',
                            'asb_klinik_admission_registration',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'views/views.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : True,
}

