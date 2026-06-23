from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ReassignWizard(models.TransientModel):
    _name = 'reassign.wizard'
    _description = 'Wizard de réaffectation'

    equipment_id = fields.Many2one('it.equipment', string="Équipement", required=True)
    employee_id = fields.Many2one('hr.employee', string="Nouvel employé", required=True)
    department_id = fields.Many2one('hr.department', string="Nouveau département", required=True)
    reason = fields.Char(string="Motif", required=True)

    def action_reassign(self):
        equipment = self.equipment_id
        old_employee = equipment.employee_id

        old_assignments = equipment.assignment_ids.filtered(lambda a: not a.end_date)
        old_assignments.write({'end_date': fields.Date.today()})

        equipment.write({
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'state': 'assigned',
        })

        self.env['it.assignment'].create({
            'equipment_id': equipment.id,
            'employee_id': self.employee_id.id,
            'department_id': self.department_id.id,
            'start_date': fields.Date.today(),
            'reason': self.reason,
        })

        return {
            'type': 'ir.actions.act_window_close',
        }
