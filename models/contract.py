from odoo import models, fields, api, _
from datetime import date


class ItContract(models.Model):
    _name = 'it.contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Contrat fournisseur'
    _order = 'end_date asc'

    name = fields.Char(string="Nom du contrat", required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string="Fournisseur", required=True, tracking=True)
    start_date = fields.Date(string="Date de début", required=True, tracking=True)
    end_date = fields.Date(string="Date de fin", required=True, tracking=True)
    amount = fields.Float(string="Montant", tracking=True)
    equipment_ids = fields.One2many('it.equipment', 'contract_id', string="Équipements couverts")
    days_remaining = fields.Integer(string="Jours restants", compute='_compute_days_remaining', store=True)
    state = fields.Selection([
        ('active', 'Actif'),
        ('expired', 'Expiré'),
        ('renewed', 'Renouvelé'),
    ], string="État", default='active', tracking=True)

    @api.depends('end_date')
    def _compute_days_remaining(self):
        for rec in self:
            if rec.end_date:
                delta = rec.end_date - date.today()
                rec.days_remaining = delta.days
            else:
                rec.days_remaining = 0

    def action_renew(self):
        self.ensure_one()
        return {
            'name': _('Renouvellement de contrat'),
            'type': 'ir.actions.act_window',
            'res_model': 'renew.contract.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_contract_id': self.id},
        }

    def cron_check_expiry(self):
        expiring = self.search([('state', '=', 'active'), ('end_date', '<=', fields.Date.today())])
        expiring.write({'state': 'expired'})
