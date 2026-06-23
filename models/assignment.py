from odoo import models, fields, api


class ItAssignment(models.Model):
    _name = 'it.assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Historique des affectations'
    _order = 'start_date desc'

    equipment_id = fields.Many2one('it.equipment', string="Équipement", required=True, tracking=True)
    employee_id = fields.Many2one('hr.employee', string="Employé", required=True, tracking=True)
    department_id = fields.Many2one('hr.department', string="Département", required=True, tracking=True)
    start_date = fields.Date(string="Date de début", required=True, default=fields.Date.today, tracking=True)
    end_date = fields.Date(string="Date de fin", tracking=True)
    reason = fields.Char(string="Motif", tracking=True)
