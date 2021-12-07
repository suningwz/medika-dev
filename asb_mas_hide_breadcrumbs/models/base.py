# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Base(models.AbstractModel):
    _inherit = 'base'
    _description = 'Base'

    def get_formview_action(self, access_uid=None):
        """ Override this method in order to redirect many2one towards the right model depending on access_uid """
        res = super(Base, self).get_formview_action(access_uid=access_uid)
        if self._name == 'res.partner':
            if self.client or self.provide or self.member or self.is_pic:
                res.update({
                    'target': 'main'
                })
        # name = [
        if self._name in [
            'benefit.benefit',
            'bank.master',
            'benefit.master',
            'edc.master',
            'provider.activity',
            'facility.category',
            'provider.facility',
            'provider.facility.line',
            'master.remarks',
            'diagnosis.diagnosis',
            'diagnosis.root',
            'provider.provider',
            'provider.contract',
            'correspondence.correspondence',
            'correspondence.type',
            'provider.discount',
            'discount.benefit',
            'rebate.detail',
            'rebate.benefit',
            'member.deleted',
            'remarks.member.deleted',
            'client.activity',
            'client.activity.line',
            'client.branch',
            'client.program',
            'client.program.plan',
            'client.program.plan.line',
            'client.program.floatfund',
            'program.plan.header',
            'header.detail',
            'activity.participant',
            'client.terms.conditions',
            'edit.program',
            'edit.floatfund',
            'edit.plan',
            'edit.program.plan',
            'edit.program.plan.line',
            'edit.program.plan.header',
            'edit.header.detail',
            'suffix.id',
            'plan.information',
            'member.history',
            'card.number',
            'member.benefit.limit',
            'member.deductible.remaning',
            'member.per.day.limit',
            'policy.policy',
            'policy.member.line',
            'policy.member.wizard',
            'eclaim.batch',
            'eclaim.document',
            'eclaim.eclaim',
            'eclaim.invoice.detail',
            'eclaim.invoice.wizard',
            'invoice.detail.item',
            'eclaim.item.type',
            'eclaim.item',
            'call.record',
            'call.record.lines',
            'helpline.source',
            'ticketing.information',
            'case.monitoring',
            'monitoring.detail.remarks',
            'monitoring.detail',
            'cost.contaiment.line',
            'case.monitoring.chart',
            'guarantee.letter',
            'final.gl',
            'claim.reject.reason',
            'issued.issued',
            'monitoring.detail.remarks',
            'monitoring.detail',
            'cost.contaiment.line',
            'case.monitoring.chart',
            'pre.admission',
            'helpline.source',
            'helpline.supporting.ambulance.rental',
            'helpline.supporting.ambulance.rs',
            'helpline.supporting.assistance',
            'helpline.supporting.eap',
            'helpline.supporting.embassy',
            'helpline.supporting.specialist',
            'import.member',
            'preview.file',
        ]:
            # for rec in name:
            # if self._name == rec:
            res.update({
                'target': 'main'
            })
        return res
