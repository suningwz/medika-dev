# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor Gigi Antrian Pasien',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor Gigi Antrian Pasien',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor Gigi Antrian Pasien',
    'description'   :   '''
                            Custom Doctor Gigi Antrian Pasien Module for Medika
                        ''',
    'depends'       : [
                        'base',
                        'mail',
                        'portal',
                        'asb_klinik_doctor_team',
                        'asb_klinik_master_cost_allocation',
                        'asb_klinik_master_poli_unit',
                        'asb_klinik_master_fasilitas_kesehatan',
                        'asb_klinik_master_ketenagaan',
                        'asb_klinik_master_personil',
                        'asb_klinik_master_product',
                        'asb_klinik_costing_package',
                        'asb_klinik_costing_setting_general',
                        'asb_klinik_costing_setting_onsite',
                        'asb_klinik_admission_reservation',
                        'asb_klinik_admission_registration',
                        'asb_klinik_admission_poli_perawat',
                        'asb_klinik_doctor_umum_antrian_pasien',
                      ],

    'data'          : [
                        'security/doctor_gigi_security.xml',
                        'security/ir.model.access.csv',
                        'views/antrian_pasien_view.xml',
                        'views/detail_pemeriksaan_mc_view.xml',
                        'views/permintaan_lab_view.xml',
                        'views/pemeriksaan_gigi_view.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}
