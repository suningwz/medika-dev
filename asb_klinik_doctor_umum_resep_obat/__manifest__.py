# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor Umum Resep Obat',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor Resep Obat',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor Resep Obat',
    'description'   :   '''
                            Custom Doctor : Resep Obat Module for Medika
                        ''',
    'depends'       : [ 
                        'base', 
                        'mail', 
                        'portal', 
                        'asb_klinik_doctor_team',
                        'asb_klinik_master_product', 
                        'asb_klinik_doctor_umum_antrian_pasien',
                      ],

    'data'          : [
                        'security/ir.model.access.csv',
                        'views/master_registration_views.xml',
                        'views/resep_obat_views.xml',
                        'views/detail_obat_views.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}
