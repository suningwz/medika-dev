# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, ValidationError


class DiagnosisDiagnosis(models.Model):
    _name = 'diagnosis.diagnosis'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Diagnosis Diagnosis'

    name = fields.Char('Diagnosis Name', required=True, tracking=True, store=True,)
    diagnosis_code = fields.Char(string='Code', tracking=True, store=True,)
    description = fields.Char(string='Description', tracking=True, store=True,)
    edc_code = fields.Char(string='EDC Code', tracking=True, store=True,)
    initial_symptom = fields.Char(string='Initial Symptom', tracking=True, store=True,)
    vital_sign = fields.Char(string='Vital Sign', tracking=True, store=True,)
    root_id = fields.Many2one('diagnosis.root', compute='_compute_diagnosis_root', store=True, tracking=True)
    length_stay = fields.Integer(string='Length of Stay', tracking=True, store=True)
    estimated_cost = fields.Float(string='Estimated Cost', tracking=True, store=True,)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', default=lambda self: self.env.user.company_id.currency_id.id, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner')

    def name_get(self):
        res = []
        for rec in self:
            if not rec.description:
                res.append((rec.id, '%s - %s' % (rec.diagnosis_code, rec.name)))
            else:
                res.append((rec.id, '%s - %s (%s)' % (rec.diagnosis_code, rec.name, rec.description)))
        return res

    @api.depends('diagnosis_code')
    def _compute_diagnosis_root(self):
        for record in self:
            record.diagnosis_code = record.diagnosis_code.upper()
            if ord(record.diagnosis_code[0]) > 122 or ord(record.diagnosis_code[1:2]) > 122 or ord(record.diagnosis_code[2:3]) > 122 or ord(record.diagnosis_code[4:5] or '\x00') > 122:
                raise UserError("Syntax Error! Diagnosis Code")
            else:
                record.root_id = (ord(record.diagnosis_code[0].upper()) * 1000000 + ord(record.diagnosis_code[1:2].upper()) * 10000 +
                                  ord(record.diagnosis_code[2:3].upper()) * 100 + ord(record.diagnosis_code[4:5].upper() or '\x00')) if record.diagnosis_code else False


class DiagnosisRoot(models.Model):
    _name = 'diagnosis.root'
    _description = 'Diagnosis codes first 4 digits'
    _auto = False

    name = fields.Char()
    parent_id = fields.Many2one('diagnosis.root')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (

            SELECT DISTINCT ASCII(UPPER(diagnosis_code)) * 1000000 + ASCII(SUBSTRING(diagnosis_code,2,1)) * 10000 + ASCII(SUBSTRING(diagnosis_code,3,1)) * 100 + ASCII(SUBSTRING(diagnosis_code,5,1)) AS id,
                    CONCAT(UPPER(LEFT(diagnosis_code,5)),' ',description) AS name,
                    ASCII(UPPER(diagnosis_code)) * 10000 + ASCII(SUBSTRING(diagnosis_code,2,1)) * 100 + ASCII(SUBSTRING(diagnosis_code,3,1)) AS parent_id
            FROM diagnosis_diagnosis WHERE diagnosis_code IS NOT NULL
            UNION ALL            
            
            SELECT DISTINCT ASCII(UPPER(diagnosis_code)) * 10000 + ASCII(SUBSTRING(diagnosis_code,2,1)) * 100 + ASCII(SUBSTRING(diagnosis_code,3,1)) AS id,
                   CONCAT(UPPER(LEFT(diagnosis_code,3)),' ',name) AS name,
                   NULL::int AS parent_id
            FROM diagnosis_diagnosis WHERE diagnosis_code IS NOT NULL
            
            )''' % (self._table,)
        )
