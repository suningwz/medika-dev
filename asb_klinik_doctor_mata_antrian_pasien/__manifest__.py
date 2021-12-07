# -*- coding: utf-8 -*-
{
    'name'          : 'Doctor Mata Antrian Pasien',
    'version'       : '0.1',
    'author'        : 'PT Arkana Solusi Bisnis',
    'license'       : 'OPL-1',
    'category'      : 'Doctor Mata Antrian Pasien',
    'website'       : 'http://www.arkana.co.id',
    'summary'       : 'Custom Doctor Mata Antrian Pasien',
    'description'   :   '''
                            Custom Doctor Mata Antrian Pasien Module for Medika
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
                        'security/doctor_mata_security.xml',
                        'security/ir.model.access.csv',
                        'views/antrian_pasien_view.xml',
                        'views/detail_pemeriksaan_mc_view.xml',
                        'views/permintaan_lab_view.xml',
                        'views/pemeriksaan_mata_view.xml',
                      ],
    'installable'   : True,
    'auto_install'  : False,
    'application'   : False,
}
