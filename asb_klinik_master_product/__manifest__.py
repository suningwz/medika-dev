# -*- coding: utf-8 -*-
{
    'name'          :   "Master Product Klinik",

    'summary'       :   """
                        Module Master Product Klinik
                        """,

    'description'   :   """
                        Module Master Product Klinik
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
                            'product',
                            'stock',
                            'tgl_format_number',
                            'asb_klinik_master_cost_allocation',
                            'asb_klinik_master_poli_unit',
                            'asb_klinik_master_fasilitas_kesehatan',
                            'asb_klinik_master_personil',
                        ],

    # always loaded
    'data'          :   [
                            'security/ir.model.access.csv',
                            'data/master_kategori_produk_data.xml',
                            'data/master_komponen_tarif_data.xml',
                            'views/config_bentuk_persediaan_view.xml',
                            'views/config_sub_kategori_produk.xml',
                            'views/master_kategori_produk_view.xml',
                            'views/master_komponen_tarif_view.xml',
                            'views/master_alat_obat_view.xml',
                            'views/master_jasa_view.xml',
                            'views/master_tindakan_layanan_view.xml',
                            'views/master_sampling_view.xml',
                            'views/master_pricelist_view.xml',                            
                            'data/data_kategori_produk.xml',
                            'data/data_komponen_tarif.xml',
                            'data/data_bentuk_persediaan_obat.xml',
                        ],
    'installable'   : True,
    'auto_install'  : False,
}
