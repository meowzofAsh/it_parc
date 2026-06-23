import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ItParcDashboard extends Component {
    static template = "it_parc.Dashboard";

    setup() {
        this.state = useState({ kpis: {} });
        onWillStart(async () => {
            const data = await this.env.services.orm.call(
                "it.equipment", "get_dashboard_data"
            );
            this.state.kpis = data;
        });
    }
}

registry.category("actions").add("it_parc.dashboard", ItParcDashboard);
