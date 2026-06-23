import { Component, useState, onWillStart, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";

const CHART_COLORS = [
    "#7c7bad", "#5ab0a0", "#e9a05a", "#d96c6c", "#6ba8d9", "#a87dc9"
];

export class ItParcDashboard extends Component {
    static template = "it_parc.Dashboard";

    setup() {
        this.state = useState({ kpis: {} });
        this.chart = null;

        onWillStart(async () => {
            const data = await this.env.services.orm.call(
                "it.equipment", "get_dashboard_data"
            );
            this.state.kpis = data;
        });

        onMounted(() => this._renderChart());
    }

    _renderChart() {
        const data = this.state.kpis;
        if (!data.chart_labels || !data.chart_values) return;

        const canvas = this.el.querySelector("#dashboardChart");
        if (!canvas) return;

        if (this.chart) {
            this.chart.destroy();
        }

        const ctx = canvas.getContext("2d");
        const Chart = window.Chart;

        if (!Chart) {
            console.warn("Chart.js not loaded");
            return;
        }

        this.chart = new Chart(ctx, {
            type: "doughnut",
            data: {
                labels: data.chart_labels,
                datasets: [{
                    data: data.chart_values,
                    backgroundColor: CHART_COLORS.slice(0, data.chart_labels.length),
                    borderWidth: 2,
                    borderColor: "#fff",
                }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: { padding: 16, usePointStyle: true },
                    },
                    title: {
                        display: true,
                        text: "Répartition par catégorie",
                        font: { size: 16, weight: "bold" },
                        padding: { bottom: 16 },
                    },
                },
            },
        });
    }
}

registry.category("actions").add("it_parc.dashboard", ItParcDashboard);
