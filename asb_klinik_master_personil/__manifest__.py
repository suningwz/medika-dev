# -*- coding: utf-8 -*-
{
    'name'          :   "Master Personil Klinik",

    'summary'       :   """
                        Module Master Personil Klinik
                        """,

    'description'   :   """
                        Module Master Personil Klinik
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
                            'l10n_id_efaktur',
                            'base', 
                            'mail',
                            'account',
                            'asb_state_city',
                            'contacts_maps',
                            'web_widget_image_webcam',
                            'asb_klinik_master_dokumen',
                            'asb_master_configuration_pic_title',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'data/master_personil_data.xml',
                            'views/config_lokasi_pekerjaan_view.xml',
                            'views/config_jenis_pekerjaan_view.xml',
                            'views/master_dokter_view.xml',
                            'views/master_perawat_view.xml',
                            'views/master_non_medis_view.xml',
                            'views/master_pic_perusahaan_view.xml',
                            'views/master_perusahaan_view.xml',
                            'views/master_pasien_view.xml',
                            'views/master_personil_action_view.xml',
                            'views/master_dokumen_view.xml',
                            'data/master_jenis_pekerjaan_data.xml',
                            'data/master_lokasi_pekerjaan_data.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
