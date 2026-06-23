from odoo import models, fields, api, _


class RenewContractWizard(models.TransientModel):
    _name = 'renew.contract.wizard'
    _description = 'Wizard de renouvellement de contrat'

    contract_id = fields.Many2one('it.contract', string="Contrat", required=True)
    new_end_date = fields.Date(string="Nouvelle date de fin", required=True)
    new_amount = fields.Float(string="Nouveau montant")

    def action_renew(self):
        contract = self.contract_id
        contract.write({
            'state': 'renewed',
        })

        new_contract = contract.copy(default={
            'start_date': contract.end_date,
            'end_date': self.new_end_date,
            'amount': self.new_amount or contract.amount,
            'state': 'active',
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'it.contract',
            'res_id': new_contract.id,
            'view_mode': 'form',
        }
