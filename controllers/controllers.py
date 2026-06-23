from odoo import http
from odoo.http import request


class DashboardController(http.Controller):

    @http.route('/it_parc/dashboard/data', type='jsonrpc', auth='user', methods=['POST'])
    def get_dashboard_data(self, **kwargs):
        Equipment = request.env['it.equipment']
        Intervention = request.env['it.intervention']

        total_equipments = Equipment.search_count([])
        total_value = sum(Equipment.search_read([], ['purchase_value']) or [], 0)
        return {
            'total_equipments': total_equipments,
            'total_value': total_value,
        }
