from odoo import models, fields, api


class ReassignWizard(models.TransientModel):
    _name = 'reassign.wizard'
    _description = 'Wizard de réaffectation'

    equipment_id = fields.Many2one('it.equipment', string="Équipement", required=True)
    employee_id = fields.Many2one('hr.employee', string="Nouvel employé", required=True)
    department_id = fields.Many2one('hr.department', string="Nouveau département", required=True)
    reason = fields.Char(string="Motif", required=True)

    def action_reassign(self):
        self.equipment_id.write({
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}
