# -*- coding: utf-8 -*-

# import odoo.exceptions
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class EclaimEclaim(models.Model):
    _inherit = 'eclaim.eclaim'

    def action_batch(self):
        for rec in self:
            batch = []
            batch_vals = {}
            client_member = []
            # client_nonmember = []
            member = 'non_member'
            payment = 'provider'
            for line in rec.letter_ids:
                if line.service_type != rec.claim_type:
                    raise ValidationError(_("Claim type does not match for %s " % line.claim_number))
                if rec.provider_id:
                    if line.provider_id != rec.provider_id:
                        raise ValidationError(_("Provider does not match for %s " % line.provider_id))
                if rec.client_id:
                    if line.client_id != rec.client_id:
                        raise ValidationError(_("Client does not match for %s " % line.client_id))
                if line.service_type == 'reimburse':
                    payment = 'member'
                if line.member:
                    member = 'member'
                    if line.client_id in client_member:
                        # Get existing batch
                        # existing_batch = rec.letter_ids.search([('client_id', '=', line.client_id.id), ('member', '=', line.member), ('batch_id', '!=', False)])
                        for letter in rec.letter_ids:
                            if letter.client_id == line.client_id and letter.member == line.member and letter.batch_id != False:
                                existing_batch = letter
                                break
                        line.batch_id = existing_batch.batch_id.id
                        existing_batch.batch_id.letter_ids += line
                    elif line.client_id not in client_member:
                        # Create new batch
                        batch_vals = {
                            'provider_id': rec.provider_id.id,
                            'client_id': line.client_id.id,
                            'claim_type': line.service_type,
                            'receive_date': rec.receive_date,
                            'invoice_number': rec.invoice_number,
                            'client_type': member,
                            'payment': payment,
                        }
                        batch = self.env['eclaim.batch'].create(batch_vals)
                        client_member.append(line.client_id)
                        line.batch_id = batch.id
                        batch.letter_ids += line
                if not line.member:
                # if line.client_id in client_nonmember:
                #     # Get existing batch
                #     for letter in rec.letter_ids:
                #         if letter.client_id == line.client_id and letter.member == line.member and letter.batch_id != False:
                #             existing_batch = letter
                #             break
                #     line.batch_id = existing_batch.batch_id.id
                #     existing_batch.batch_id.letter_ids += line
                # elif line.client_id not in client_nonmember:
                    # Create new batch
                    batch_vals = {
                        'provider_id': rec.provider_id.id,
                        'client_id': line.client_id.id,
                        'claim_type': line.service_type,
                        'receive_date': rec.receive_date,
                        'invoice_number': rec.invoice_number,
                        'client_type': member,
                        'payment': payment,
                    }
                    batch = self.env['eclaim.batch'].create(batch_vals)
                    # client_nonmember.append(line.client_id)
                    line.batch_id = batch.id
                    batch.letter_ids += line
                rec.write({'state': 'batch'})
                line.claim_status = 'verified'
                line.receive_date = rec.receive_date
