# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor Umum Biaya MC',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor Biaya MC',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor Biaya MC',
    'description'   :   '''
                            Custom Doctor : Biaya MC Module for Medika
                        ''',
    'depends'       : [
                        'base', 
                        'mail', 
                        'portal',
                        'asb_klinik_doctor_umum_antrian_pasien', 
                        'asb_klinik_doctor_umum_resep_obat',
                      ],
    'data'          : [
                        # 'security/ir.model.access.csv',
                        'views/assets.xml',
                        'views/biaya_mc_views.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}
