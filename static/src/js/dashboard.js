import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ItParcDashboard extends Component {
    static template = "it_parc.Dashboard";

    setup() {
        this.state = useState({ kpis: {}, charts: {} });
        onWillStart(async () => {
            const data = await this.env.services.orm.call(
                "it_parc.dashboard", "get_statistics"
            );
            Object.assign(this.state, data);
        });
    }
}

registry.category("actions").add("it_parc.dashboard", ItParcDashboard);
