from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ItIntervention(models.Model):
    _name = 'it.intervention'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Intervention de maintenance'
    _order = 'start_date desc'

    equipment_id = fields.Many2one('it.equipment', string="Équipement", required=True, tracking=True)
    type = fields.Selection([
        ('corrective', 'Corrective'),
        ('preventive', 'Préventive'),
    ], string="Type", required=True, default='corrective', tracking=True)
    technician_id = fields.Many2one('hr.employee', string="Technicien", required=True, tracking=True)
    start_date = fields.Datetime(string="Date de début", required=True, tracking=True)
    end_date = fields.Datetime(string="Date de fin", tracking=True)
    duration = fields.Float(string="Durée (heures)", compute='_compute_duration', store=True)
    cost = fields.Float(string="Coût", tracking=True)
    report = fields.Html(string="Rapport d'intervention")
    state = fields.Selection([
        ('planned', 'Planifiée'),
        ('in_progress', 'En cours'),
        ('done', 'Terminée'),
    ], string="État", default='planned', tracking=True)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                delta = rec.end_date - rec.start_date
                rec.duration = delta.total_seconds() / 3600
            else:
                rec.duration = 0

    @api.constrains('cost')
    def _check_cost(self):
        for rec in self:
            if rec.cost and rec.cost < 0:
                raise ValidationError(_("Le coût ne peut pas être négatif."))

    def action_start(self):
        self.state = 'in_progress'
        self.equipment_id.state = 'maintenance'

    def action_done(self):
        self.state = 'done'
        if not self.end_date:
            self.end_date = fields.Datetime.now()
        if self.equipment_id.intervention_ids.filtered(lambda i: i.state not in ('done',)):
            return
        self.equipment_id.state = 'assigned'
