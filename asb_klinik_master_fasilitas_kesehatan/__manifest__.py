# -*- coding: utf-8 -*-
{
    'name'          :   "Master Fasilitas Kesehatan Klinik",

    'summary'       :   """
                        Module Master Fasilitas Kesehatan Klinik
                        """,

    'description'   :   """
                        Module Master Fasilitas Kesehatan Klinik
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
                            'asb_state_city', 
                            'asb_klinik_master_poli_unit',
                            'asb_klinik_master_personil',
                            'asb_klinik_master_dokumen',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'data/master_fasilitas_kesehatan_data.xml',
                            'views/master_fasilitas_kesehatan_view.xml',
                            'views/master_dokumen_view.xml',
                            'views/res_users_view.xml'
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
