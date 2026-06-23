from odoo import http
from odoo.http import request


class DashboardController(http.Controller):

    @http.route('/it_parc/dashboard/data', type='jsonrpc', auth='user', methods=['POST'])
    def get_dashboard_data(self, **kwargs):
        Equipment = request.env['it.equipment']
        return Equipment.get_dashboard_data()
