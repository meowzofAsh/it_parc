from odoo import models, fields, api


class RenewContractWizard(models.TransientModel):
    _name = 'renew.contract.wizard'
    _description = 'Wizard de renouvellement de contrat'

    contract_id = fields.Many2one('it.contract', string="Contrat", required=True)
    new_end_date = fields.Date(string="Nouvelle date de fin", required=True)
    new_amount = fields.Float(string="Nouveau montant")

    def action_renew(self):
        return {'type': 'ir.actions.act_window_close'}
