import { useEffect, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  Bell,
  Factory,
  Gauge,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  TrendingDown,
  TrendingUp,
  Wrench,
  ChevronRight,
  Database,
  CheckCircle2,
  Clock3,
  User,
  Server,
  Lock,
  FileText,
  Code2,
} from "lucide-react";

import {
  BarChart,
  Bar,
  CartesianGrid,
  Cell,
  LineChart,
  Line,
  PieChart,
  Pie,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import "./App.css";

const API_URL = "http://localhost:8000";

const chartTickStyle = {
  fontFamily: "Times New Roman, Times, serif",
  fontSize: 14,
  fill: "#28301d",
};

const tooltipStyle = {
  fontFamily: "Times New Roman, Times, serif",
  fontSize: 14,
};

const badgeStyle = {
  fontFamily: "Times New Roman, Times, serif",
  fontSize: 13,
  fontWeight: 600,
};


/* ============================================================
   COMMON COMPONENTS
   ============================================================ */

function KpiCard({ icon: Icon, title, value, trend, trendDown }) {
  return (
    <div className="kpi-card">
      <div className="kpi-top">
        <div className="kpi-icon">
          <Icon size={18} />
        </div>

        <div className={trendDown ? "trend negative" : "trend positive"}>
          {trendDown ? (
            <TrendingDown size={14} />
          ) : (
            <TrendingUp size={14} />
          )}
          {trend}
        </div>
      </div>

      <div className="kpi-value">{value}</div>
      <div className="kpi-title">{title}</div>
    </div>
  );
}


function SettingRow({
  icon: Icon,
  label,
  value,
  description,
  status,
  statusType = "success",
}) {
  return (
    <div className="setting-row">
      <div className="setting-icon">
        <Icon size={17} />
      </div>

      <div className="setting-info">
        <strong>{label}</strong>

        {description && (
          <span>{description}</span>
        )}
      </div>

      <div className="setting-value">
        <strong>{value}</strong>

        {status && (
          <span
            className={`status-badge ${
              statusType === "success"
                ? "low"
                : statusType === "warning"
                  ? "medium"
                  : "high"
            }`}
          >
            {status}
          </span>
        )}
      </div>
    </div>
  );
}


/* ============================================================
   DASHBOARD PAGE
   ============================================================ */

function DashboardPage({
  kpis,
  productionData,
  facilityData,
  riskData,
  maintenanceAlerts,
  loading,
}) {
  const formatProduction = (value) => {
    if (value === undefined || value === null) return "--";
    return `${(value / 1000000).toFixed(2)}M`;
  };

  const formatNumber = (value) => {
    if (value === undefined || value === null) return "--";
    return Number(value).toLocaleString("en-US");
  };

  const riskTotal = riskData.reduce(
    (total, item) => total + item.value,
    0
  );

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Operational Overview</h2>
          <p>
            Monitor production performance, machine health and
            operational risk.
          </p>
        </div>

        <div className="period-label">Full Year</div>
      </div>

      <div className="kpi-grid">
        <KpiCard
          icon={Gauge}
          title="Production Efficiency"
          value={
            loading
              ? "--"
              : `${kpis?.production_efficiency?.toFixed(2)}%`
          }
          trend="+2.4%"
        />

        <KpiCard
          icon={Factory}
          title="Total Production"
          value={
            loading ? "--" : formatProduction(kpis?.total_production)
          }
          trend="+6.8%"
        />

        <KpiCard
          icon={TrendingDown}
          title="Downtime"
          value={
            loading
              ? "--"
              : `${formatNumber(
                  Math.round(kpis?.downtime_hours)
                )} hrs`
          }
          trend="-4.2%"
          trendDown
        />

        <KpiCard
          icon={AlertTriangle}
          title="Defect Rate"
          value={
            loading
              ? "--"
              : `${kpis?.defect_rate?.toFixed(2)}%`
          }
          trend="-0.7%"
          trendDown
        />
      </div>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Production Performance</h3>
              <p>Actual production compared with target</p>
            </div>

            <span className="panel-filter">Monthly</span>
          </div>

          <div className="chart-container">
            {productionData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={productionData}>
                  <CartesianGrid
                    strokeDasharray="3 3"
                    vertical={false}
                  />

                  <XAxis
                    dataKey="month"
                    tick={chartTickStyle}
                  />

                  <YAxis
                    tick={chartTickStyle}
                    tickFormatter={(value) =>
                      `${Math.round(value / 1000)}k`
                    }
                  />

                  <Tooltip
                    formatter={(value) =>
                      Number(value).toLocaleString("en-US")
                    }
                    contentStyle={tooltipStyle}
                  />

                  <Line
                    type="monotone"
                    dataKey="actual"
                    stroke="#66734a"
                    strokeWidth={3}
                    dot={{ r: 4 }}
                    name="Actual Production"
                  />

                  <Line
                    type="monotone"
                    dataKey="target"
                    stroke="#a8b18a"
                    strokeWidth={2}
                    strokeDasharray="5 5"
                    dot={false}
                    name="Production Target"
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <div className="chart-loading">
                Loading production data...
              </div>
            )}
          </div>
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Facility Efficiency</h3>
              <p>Average production efficiency</p>
            </div>
          </div>

          <div className="chart-container">
            {facilityData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={facilityData}
                  layout="vertical"
                  margin={{
                    top: 5,
                    right: 10,
                    left: 5,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                    horizontal={false}
                  />

                  <XAxis
                    type="number"
                    domain={[0, 100]}
                    tickFormatter={(value) => `${value}%`}
                    tick={chartTickStyle}
                  />

                  <YAxis
                    type="category"
                    dataKey="facility"
                    width={140}
                    tick={chartTickStyle}
                  />

                  <Tooltip
                    formatter={(value) => `${value}%`}
                    contentStyle={tooltipStyle}
                  />

                  <Bar
                    dataKey="average_efficiency"
                    fill="#66734a"
                    radius={[0, 5, 5, 0]}
                    barSize={20}
                  />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="chart-loading">
                Loading facility data...
              </div>
            )}
          </div>
        </section>
      </div>

      <div className="bottom-row">
        <section className="panel risk-panel">
          <div className="panel-header">
            <div>
              <h3>Machine Risk Distribution</h3>
              <p>Current ML-based maintenance risk</p>
            </div>

            <span
              className="reading-count"
              style={badgeStyle}
            >
              {riskTotal.toLocaleString()} readings
            </span>
          </div>

          <div className="risk-content">
            <div className="risk-chart">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={55}
                    outerRadius={80}
                    paddingAngle={3}
                  >
                    <Cell fill="#68764c" />
                    <Cell fill="#b69a52" />
                    <Cell fill="#8c5145" />
                  </Pie>

                  <Tooltip contentStyle={tooltipStyle} />
                </PieChart>
              </ResponsiveContainer>

              <div className="risk-center">
                <strong>
                  {riskTotal.toLocaleString()}
                </strong>

                <span>Readings</span>
              </div>
            </div>

            <div className="risk-legend">
              {riskData.map((risk) => (
                <div key={risk.name}>
                  <span
                    className={`legend-dot ${risk.name
                      .toLowerCase()
                      .replace(" risk", "")}`}
                  />

                  <span>{risk.name}</span>

                  <strong>
                    {risk.value.toLocaleString()}
                  </strong>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="panel alerts-panel">
          <div className="panel-header">
            <div>
              <h3>Maintenance Alerts</h3>
              <p>Machines requiring attention</p>
            </div>

            <span
              className="alert-count"
              style={badgeStyle}
            >
              {maintenanceAlerts.length} alerts
            </span>
          </div>

          <div className="machine-list">
            {maintenanceAlerts.length === 0 ? (
              <div className="chart-loading">
                No machines currently require attention.
              </div>
            ) : (
              maintenanceAlerts.map((machine) => (
                <div
                  className="machine-row"
                  key={machine.machine_id}
                >
                  <div className="machine-icon">
                    <Wrench size={16} />
                  </div>

                  <div className="machine-info">
                    <strong>{machine.machine_name}</strong>
                    <span>{machine.production_line}</span>
                  </div>

                  <div
                    className={`machine-risk ${machine.risk_level.toLowerCase()}`}
                  >
                    {(machine.failure_probability * 100).toFixed(0)}%
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </>
  );
}


/* ============================================================
   PRODUCTION PAGE
   ============================================================ */

function ProductionPage({ productionData, facilityData }) {
  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Production</h2>
          <p>
            Production output and facility performance across the
            manufacturing network.
          </p>
        </div>
      </div>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Monthly Production</h3>
              <p>Actual output compared with production target</p>
            </div>
          </div>

          <div className="large-chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={productionData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="month"
                  tick={chartTickStyle}
                />

                <YAxis
                  tick={chartTickStyle}
                  tickFormatter={(value) =>
                    `${Math.round(value / 1000)}k`
                  }
                />

                <Tooltip
                  formatter={(value) =>
                    Number(value).toLocaleString("en-US")
                  }
                  contentStyle={tooltipStyle}
                />

                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="#66734a"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                  name="Actual Production"
                />

                <Line
                  type="monotone"
                  dataKey="target"
                  stroke="#a8b18a"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={false}
                  name="Production Target"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Facility Performance</h3>
            <p>Production and operational performance by facility</p>
          </div>
        </div>

        <div className="data-table">
          <div className="table-row table-header">
            <span>Facility</span>
            <span>Actual Production</span>
            <span>Target</span>
            <span>Efficiency</span>
            <span>Downtime</span>
          </div>

          {facilityData.map((facility) => (
            <div className="table-row" key={facility.facility}>
              <strong>{facility.facility}</strong>

              <span>
                {Number(facility.actual_production).toLocaleString()}
              </span>

              <span>
                {Number(facility.production_target).toLocaleString()}
              </span>

              <span className="efficiency-value">
                {facility.average_efficiency}%
              </span>

              <span>
                {Number(facility.downtime_hours).toLocaleString()} hrs
              </span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}


/* ============================================================
   MACHINE HEALTH PAGE
   ============================================================ */

function MachineHealthPage({ machineHealth }) {
  const highRisk = machineHealth.filter(
    (machine) => machine.risk_level === "High"
  ).length;

  const mediumRisk = machineHealth.filter(
    (machine) => machine.risk_level === "Medium"
  ).length;

  const lowRisk = machineHealth.filter(
    (machine) => machine.risk_level === "Low"
  ).length;

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Machine Health</h2>
          <p>
            Monitor machine condition and ML-based predictive
            maintenance risk.
          </p>
        </div>
      </div>

      <div className="health-summary">
        <div className="health-card">
          <span>Total Machines</span>
          <strong>{machineHealth.length}</strong>
        </div>

        <div className="health-card">
          <span>High Risk</span>
          <strong>{highRisk}</strong>
        </div>

        <div className="health-card">
          <span>Medium Risk</span>
          <strong>{mediumRisk}</strong>
        </div>

        <div className="health-card">
          <span>Low Risk</span>
          <strong>{lowRisk}</strong>
        </div>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Machine Health Monitoring</h3>
            <p>
              Latest sensor readings and predictive maintenance risk
            </p>
          </div>

          <span
            className="reading-count"
            style={badgeStyle}
          >
            {machineHealth.length} machines
          </span>
        </div>

        {machineHealth.length === 0 ? (
          <div className="chart-loading">
            Loading machine health data...
          </div>
        ) : (
          <div className="maintenance-table">
            <div className="maintenance-header">
              <span>Machine</span>
              <span>Status</span>
              <span>Temperature</span>
              <span>Vibration</span>
              <span>Risk</span>
              <span>Probability</span>
              <span>Action</span>
            </div>

            {machineHealth.map((machine) => (
              <div
                className="maintenance-row"
                key={machine.machine_id}
              >
                <div>
                  <strong>{machine.machine_name}</strong>
                  <span>{machine.machine_type}</span>
                </div>

                <span>{machine.operating_status}</span>

                <span>{machine.temperature}°</span>

                <span>{machine.vibration}</span>

                <span
                  className={`status-badge ${machine.risk_level.toLowerCase()}`}
                >
                  {machine.risk_level}
                </span>

                <strong>
                  {(machine.failure_probability * 100).toFixed(1)}%
                </strong>

                <span className="health-action">
                  {machine.recommendation}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}


/* ============================================================
   MAINTENANCE PAGE
   ============================================================ */

function MaintenancePage({ maintenanceAlerts }) {
  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Maintenance</h2>
          <p>
            Machines currently requiring inspection or maintenance
            attention.
          </p>
        </div>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Maintenance Alerts</h3>
            <p>Current machine risk requiring operational attention</p>
          </div>

          <span
            className="alert-count"
            style={badgeStyle}
          >
            {maintenanceAlerts.length} alerts
          </span>
        </div>

        {maintenanceAlerts.length === 0 ? (
          <div className="chart-loading">
            No machines currently require maintenance attention.
          </div>
        ) : (
          <div className="maintenance-table">
            <div className="maintenance-header">
              <span>Machine</span>
              <span>Production Line</span>
              <span>Risk Level</span>
              <span>Failure Probability</span>
              <span>Action</span>
            </div>

            {maintenanceAlerts.map((machine) => (
              <div
                className="maintenance-row"
                key={machine.machine_id}
              >
                <strong>{machine.machine_name}</strong>

                <span>{machine.production_line}</span>

                <span
                  className={`status-badge ${machine.risk_level.toLowerCase()}`}
                >
                  {machine.risk_level}
                </span>

                <strong>
                  {(machine.failure_probability * 100).toFixed(1)}%
                </strong>

                <button className="action-button">
                  Review
                  <ChevronRight size={15} />
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}


/* ============================================================
   ANALYTICS PAGE
   ============================================================ */

function AnalyticsPage({
  productionAnalytics,
  downtimeAnalytics,
  qualityAnalytics,
  machineAnalytics,
  analyticsLoading,
}) {
  if (analyticsLoading) {
    return (
      <>
        <div className="page-heading">
          <div>
            <h2>Analytics</h2>
            <p>
              Deeper analysis of production, downtime, quality and
              machine operations.
            </p>
          </div>

          <div className="period-label">Full Year</div>
        </div>

        <section className="panel full-panel">
          <div className="chart-loading">
            Loading analytical data...
          </div>
        </section>
      </>
    );
  }

  if (
    !productionAnalytics ||
    !downtimeAnalytics ||
    !qualityAnalytics ||
    !machineAnalytics
  ) {
    return (
      <>
        <div className="page-heading">
          <div>
            <h2>Analytics</h2>
            <p>
              Deeper analysis of production, downtime, quality and
              machine operations.
            </p>
          </div>
        </div>

        <section className="panel full-panel">
          <div className="chart-loading">
            Analytics data is currently unavailable.
          </div>
        </section>
      </>
    );
  }

  const monthlyProduction = productionAnalytics.monthly || [];
  const facilityProduction = productionAnalytics.facility || [];

  const facilityDowntime = downtimeAnalytics.facility || [];
  const productionLineDowntime =
    downtimeAnalytics.production_line || [];

  const facilityQuality = qualityAnalytics.facility || [];
  const monthlyQuality = qualityAnalytics.monthly || [];

  const sensorSummary =
    machineAnalytics.sensor_summary || [];

  const maintenanceByMachine =
    machineAnalytics.maintenance_by_machine || [];

  const maintenanceTypes =
    machineAnalytics.maintenance_types || [];

  const riskByMachineType =
    machineAnalytics.risk_by_machine_type || [];

  const productionSummary =
    productionAnalytics.summary || {};

  const downtimeSummary =
    downtimeAnalytics.summary || {};

  const productionInsight =
    productionAnalytics.insights || {};

  const downtimeInsight =
    downtimeAnalytics.insights || {};

  const qualityInsight =
    qualityAnalytics.insights || {};

  const machineInsight =
    machineAnalytics.insights || {};

  const highestDefectFacility = [...facilityQuality].sort(
    (a, b) => b.defect_rate - a.defect_rate
  )[0];

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Analytics</h2>
          <p>
            Deeper analysis of production, downtime, quality and
            machine operations.
          </p>
        </div>

        <div className="period-label">Full Year</div>
      </div>

      <div className="kpi-grid">
        <KpiCard
          icon={TrendingDown}
          title="Production Gap"
          value={
            productionSummary.production_gap !== undefined
              ? Number(
                  productionSummary.production_gap
                ).toLocaleString()
              : "--"
          }
          trend={
            productionSummary.gap_percentage !== undefined
              ? `${productionSummary.gap_percentage}%`
              : "--"
          }
          trendDown
        />

        <KpiCard
          icon={Factory}
          title="Actual Production"
          value={
            productionSummary.total_actual !== undefined
              ? `${(
                  productionSummary.total_actual / 1000000
                ).toFixed(2)}M`
              : "--"
          }
          trend="Actual"
        />

        <KpiCard
          icon={TrendingDown}
          title="Total Downtime"
          value={
            downtimeSummary.total_downtime_hours !== undefined
              ? `${Number(
                  downtimeSummary.total_downtime_hours
                ).toLocaleString()} hrs`
              : "--"
          }
          trend="Recorded"
          trendDown
        />

        <KpiCard
          icon={AlertTriangle}
          title="Highest Defect Rate"
          value={
            highestDefectFacility
              ? `${highestDefectFacility.defect_rate}%`
              : "--"
          }
          trend="Facility"
          trendDown
        />
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Business Findings</h3>
            <p>
              Operational observations calculated from manufacturing
              data
            </p>
          </div>
        </div>

        <div className="health-summary">
          <div className="health-card">
            <span>Largest Production Gap</span>
            <strong>
              {productionInsight.largest_facility_gap || "--"}
            </strong>
            <small>
              {productionInsight.largest_facility_gap_value !==
              undefined
                ? `${Number(
                    productionInsight.largest_facility_gap_value
                  ).toLocaleString()} units`
                : ""}
            </small>
          </div>

          <div className="health-card">
            <span>Highest Downtime Facility</span>
            <strong>
              {downtimeInsight.highest_downtime_facility || "--"}
            </strong>
            <small>
              {downtimeInsight.highest_downtime_facility_hours !==
              undefined
                ? `${Number(
                    downtimeInsight.highest_downtime_facility_hours
                  ).toLocaleString()} hrs`
                : ""}
            </small>
          </div>

          <div className="health-card">
            <span>Highest Defect Facility</span>
            <strong>
              {qualityInsight.highest_defect_facility || "--"}
            </strong>
            <small>
              {qualityInsight.highest_defect_rate !== undefined
                ? `${qualityInsight.highest_defect_rate}% defect rate`
                : ""}
            </small>
          </div>

          <div className="health-card">
            <span>Most Maintained Machine</span>
            <strong>
              {machineInsight.highest_maintenance_machine || "--"}
            </strong>
            <small>
              {machineInsight.highest_maintenance_count !== undefined
                ? `${machineInsight.highest_maintenance_count} maintenance events`
                : ""}
            </small>
          </div>
        </div>

        <div className="machine-list">
          <div className="machine-row">
            <div className="machine-icon">
              <BarChart3 size={16} />
            </div>

            <div className="machine-info">
              <strong>
                Largest monthly production gap
              </strong>

              <span>
                {productionInsight.largest_month_gap || "--"}
              </span>
            </div>

            <div className="machine-risk medium">
              {productionInsight.largest_month_gap_value !==
              undefined
                ? Number(
                    productionInsight.largest_month_gap_value
                  ).toLocaleString()
                : "--"}
            </div>
          </div>

          <div className="machine-row">
            <div className="machine-icon">
              <Wrench size={16} />
            </div>

            <div className="machine-info">
              <strong>
                Highest downtime production line
              </strong>

              <span>
                {downtimeInsight.highest_downtime_line || "--"}
              </span>
            </div>

            <div className="machine-risk high">
              {downtimeInsight.highest_downtime_line_hours !==
              undefined
                ? `${Number(
                    downtimeInsight.highest_downtime_line_hours
                  ).toLocaleString()} hrs`
                : "--"}
            </div>
          </div>

          <div className="machine-row">
            <div className="machine-icon">
              <AlertTriangle size={16} />
            </div>

            <div className="machine-info">
              <strong>
                Highest defect production line
              </strong>

              <span>
                {qualityInsight.highest_defect_line || "--"}
              </span>
            </div>

            <div className="machine-risk high">
              {qualityInsight.highest_defect_line_rate !==
              undefined
                ? `${qualityInsight.highest_defect_line_rate}%`
                : "--"}
            </div>
          </div>
        </div>
      </section>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Production Gap Analysis</h3>
              <p>
                Monthly difference between target and actual output
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyProduction}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="month"
                  tick={chartTickStyle}
                />

                <YAxis
                  tick={chartTickStyle}
                  tickFormatter={(value) =>
                    `${Math.round(value / 1000)}k`
                  }
                />

                <Tooltip
                  formatter={(value) =>
                    Number(value).toLocaleString("en-US")
                  }
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="gap"
                  fill="#8c5145"
                  radius={[5, 5, 0, 0]}
                  name="Production Gap"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Facility Production Gap</h3>
              <p>
                Production shortfall by facility
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={facilityProduction}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 20,
                  left: 5,
                  bottom: 5,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  horizontal={false}
                />

                <XAxis
                  type="number"
                  tick={chartTickStyle}
                  tickFormatter={(value) =>
                    `${Math.round(value / 1000)}k`
                  }
                />

                <YAxis
                  type="category"
                  dataKey="facility"
                  width={145}
                  tick={chartTickStyle}
                />

                <Tooltip
                  formatter={(value) =>
                    Number(value).toLocaleString("en-US")
                  }
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="gap"
                  fill="#66734a"
                  radius={[0, 5, 5, 0]}
                  barSize={20}
                  name="Production Gap"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Downtime by Facility</h3>
              <p>
                Contribution of each facility to total downtime
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={facilityDowntime}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="facility"
                  tick={chartTickStyle}
                  angle={-20}
                  textAnchor="end"
                  height={65}
                />

                <YAxis tick={chartTickStyle} />

                <Tooltip
                  formatter={(value) =>
                    `${Number(value).toLocaleString()} hrs`
                  }
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="downtime_hours"
                  fill="#8c5145"
                  radius={[5, 5, 0, 0]}
                  name="Downtime"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Production Line Downtime</h3>
              <p>
                Production lines with highest downtime
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={productionLineDowntime.slice(0, 10)}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 20,
                  left: 5,
                  bottom: 5,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  horizontal={false}
                />

                <XAxis
                  type="number"
                  tick={chartTickStyle}
                />

                <YAxis
                  type="category"
                  dataKey="production_line"
                  width={130}
                  tick={chartTickStyle}
                />

                <Tooltip
                  formatter={(value) =>
                    `${Number(value).toLocaleString()} hrs`
                  }
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="downtime_hours"
                  fill="#66734a"
                  radius={[0, 5, 5, 0]}
                  barSize={18}
                  name="Downtime"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Quality Analysis</h3>
              <p>
                Defect rate across manufacturing facilities
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={facilityQuality}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 20,
                  left: 5,
                  bottom: 5,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  horizontal={false}
                />

                <XAxis
                  type="number"
                  tick={chartTickStyle}
                  tickFormatter={(value) => `${value}%`}
                />

                <YAxis
                  type="category"
                  dataKey="facility"
                  width={145}
                  tick={chartTickStyle}
                />

                <Tooltip
                  formatter={(value) => `${value}%`}
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="defect_rate"
                  fill="#b69a52"
                  radius={[0, 5, 5, 0]}
                  barSize={20}
                  name="Defect Rate"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Quality Trend</h3>
              <p>
                Monthly defect rate
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={monthlyQuality}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="month"
                  tick={chartTickStyle}
                />

                <YAxis
                  tick={chartTickStyle}
                  tickFormatter={(value) => `${value}%`}
                />

                <Tooltip
                  formatter={(value) => `${value}%`}
                  contentStyle={tooltipStyle}
                />

                <Line
                  type="monotone"
                  dataKey="defect_rate"
                  stroke="#8c5145"
                  strokeWidth={3}
                  dot={{ r: 4 }}
                  name="Defect Rate"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Maintenance Analysis</h3>
            <p>
              Maintenance workload across individual machines
            </p>
          </div>
        </div>

        <div className="data-table">
          <div className="table-row table-header">
            <span>Machine</span>
            <span>Type</span>
            <span>Maintenance Events</span>
            <span>Average Duration</span>
          </div>

          {maintenanceByMachine.slice(0, 10).map((machine) => (
            <div
              className="table-row"
              key={machine.machine_name}
            >
              <strong>{machine.machine_name}</strong>

              <span>{machine.machine_type}</span>

              <span>
                {machine.maintenance_count}
              </span>

              <span>
                {machine.average_maintenance_duration} hrs
              </span>
            </div>
          ))}
        </div>
      </section>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Maintenance Type Distribution</h3>
              <p>
                Frequency of different maintenance activities
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={maintenanceTypes}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="maintenance_type"
                  tick={chartTickStyle}
                />

                <YAxis tick={chartTickStyle} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="count"
                  fill="#66734a"
                  radius={[5, 5, 0, 0]}
                  name="Maintenance Events"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Risk by Machine Type</h3>
              <p>
                Average predicted maintenance risk
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={riskByMachineType}
                layout="vertical"
                margin={{
                  top: 5,
                  right: 20,
                  left: 5,
                  bottom: 5,
                }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  horizontal={false}
                />

                <XAxis
                  type="number"
                  domain={[0, 1]}
                  tick={chartTickStyle}
                  tickFormatter={(value) =>
                    `${Math.round(value * 100)}%`
                  }
                />

                <YAxis
                  type="category"
                  dataKey="machine_type"
                  width={100}
                  tick={chartTickStyle}
                />

                <Tooltip
                  formatter={(value) =>
                    `${(Number(value) * 100).toFixed(1)}%`
                  }
                  contentStyle={tooltipStyle}
                />

                <Bar
                  dataKey="average_failure_probability"
                  fill="#8c5145"
                  radius={[0, 5, 5, 0]}
                  barSize={20}
                  name="Average Risk"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Machine Sensor Analysis</h3>
            <p>
              Average operating conditions by machine type
            </p>
          </div>
        </div>

        <div className="data-table">
          <div className="table-row table-header">
            <span>Machine Type</span>
            <span>Temperature</span>
            <span>Vibration</span>
            <span>Power Consumption</span>
          </div>

          {sensorSummary.map((machine) => (
            <div
              className="table-row"
              key={machine.machine_type}
            >
              <strong>
                {machine.machine_type}
              </strong>

              <span>
                {machine.avg_temperature}°
              </span>

              <span>
                {machine.avg_vibration}
              </span>

              <span>
                {machine.avg_power_consumption}
              </span>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}


/* ============================================================
   DATA QUALITY PAGE
   ============================================================ */

function DataQualityPage({
  qualitySummary,
  qualityIssues,
  validationRuns,
  dataQualityLoading,
}) {
  if (dataQualityLoading) {
    return (
      <>
        <div className="page-heading">
          <div>
            <h2>Data Quality</h2>
            <p>
              Monitor data quality issues, validation results and
              database integrity.
            </p>
          </div>
        </div>

        <section className="panel full-panel">
          <div className="chart-loading">
            Loading data quality information...
          </div>
        </section>
      </>
    );
  }

  if (!qualitySummary) {
    return (
      <>
        <div className="page-heading">
          <div>
            <h2>Data Quality</h2>
            <p>
              Monitor data quality issues, validation results and
              database integrity.
            </p>
          </div>
        </div>

        <section className="panel full-panel">
          <div className="chart-loading">
            Data quality information is currently unavailable.
          </div>
        </section>
      </>
    );
  }

  const severity = qualitySummary.severity || {};
  const latestValidation = qualitySummary.latest_validation;

  const formatDateTime = (value) => {
    if (!value) return "--";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return String(value);
    }

    return date.toLocaleString("en-US", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  };

  const severityData = [
    {
      name: "Critical",
      value: severity.critical || 0,
    },
    {
      name: "High",
      value: severity.high || 0,
    },
    {
      name: "Medium",
      value: severity.medium || 0,
    },
    {
      name: "Low",
      value: severity.low || 0,
    },
  ];

  return (
    <>
      <div className="page-heading">
        <div>
          <h2>Data Quality</h2>
          <p>
            Monitor data quality issues, validation results and
            database integrity.
          </p>
        </div>

        <div className="period-label">Current Status</div>
      </div>

      <div className="kpi-grid">
        <KpiCard
          icon={AlertTriangle}
          title="Total Issues"
          value={qualitySummary.total_issues}
          trend="Registered"
        />

        <KpiCard
          icon={Clock3}
          title="Open Issues"
          value={qualitySummary.open_issues}
          trend="Requires attention"
          trendDown={qualitySummary.open_issues > 0}
        />

        <KpiCard
          icon={CheckCircle2}
          title="Resolved Issues"
          value={qualitySummary.resolved_issues}
          trend="Completed"
        />

        <KpiCard
          icon={ShieldCheck}
          title="Critical / High"
          value={
            (severity.critical || 0) +
            (severity.high || 0)
          }
          trend={
            (severity.critical || 0) +
              (severity.high || 0) >
            0
              ? "Requires review"
              : "None"
          }
          trendDown={
            (severity.critical || 0) +
              (severity.high || 0) >
            0
          }
        />
      </div>

      <div className="charts-row">
        <section className="panel production-panel">
          <div className="panel-header">
            <div>
              <h3>Latest Validation</h3>
              <p>
                Most recent automated database quality validation
              </p>
            </div>

            {latestValidation?.validation_status === "PASSED" ? (
              <span className="status-badge low">
                PASSED
              </span>
            ) : (
              <span className="status-badge high">
                FAILED
              </span>
            )}
          </div>

          {latestValidation ? (
            <div className="health-summary">
              <div className="health-card">
                <span>Run ID</span>
                <strong>
                  #{latestValidation.run_id}
                </strong>
              </div>

              <div className="health-card">
                <span>Validation Issues</span>
                <strong>
                  {latestValidation.issue_count}
                </strong>
              </div>

              <div className="health-card">
                <span>Status</span>
                <strong>
                  {latestValidation.validation_status}
                </strong>
              </div>

              <div className="health-card">
                <span>Last Run</span>
                <strong>
                  {formatDateTime(
                    latestValidation.run_timestamp
                  )}
                </strong>
              </div>
            </div>
          ) : (
            <div className="chart-loading">
              No validation runs available.
            </div>
          )}
        </section>

        <section className="panel efficiency-panel">
          <div className="panel-header">
            <div>
              <h3>Issue Severity</h3>
              <p>
                Distribution of registered data quality issues
              </p>
            </div>
          </div>

          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={severityData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  vertical={false}
                />

                <XAxis
                  dataKey="name"
                  tick={chartTickStyle}
                />

                <YAxis
                  allowDecimals={false}
                  tick={chartTickStyle}
                />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="value"
                  fill="#66734a"
                  radius={[5, 5, 0, 0]}
                  name="Issues"
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>
      </div>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Data Quality Issues</h3>
            <p>
              Registered data quality issues identified across
              manufacturing datasets.
            </p>
          </div>

          <span
            className="reading-count"
            style={badgeStyle}
          >
            {qualityIssues.length} records
          </span>
        </div>

        {qualityIssues.length === 0 ? (
          <div className="chart-loading">
            No data quality issues have been registered.
          </div>
        ) : (
          <div className="maintenance-table">
            <div className="maintenance-header">
              <span>Dataset</span>
              <span>Record</span>
              <span>Issue</span>
              <span>Severity</span>
              <span>Status</span>
              <span>Detected</span>
            </div>

            {qualityIssues.map((issue) => (
              <div
                className="maintenance-row"
                key={issue.issue_id}
              >
                <div>
                  <strong>{issue.dataset}</strong>
                  <span>{issue.issue_type}</span>
                </div>

                <span>
                  {issue.record_identifier}
                </span>

                <div>
                  <strong>
                    {issue.issue_description}
                  </strong>
                </div>

                <span
                  className={`status-badge ${(
                    issue.severity || "low"
                  ).toLowerCase()}`}
                >
                  {issue.severity}
                </span>

                <span
                  className={`status-badge ${
                    issue.resolution_status === "Resolved"
                      ? "low"
                      : "high"
                  }`}
                >
                  {issue.resolution_status}
                </span>

                <span>
                  {formatDateTime(issue.detected_date)}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="panel full-panel">
        <div className="panel-header">
          <div>
            <h3>Validation History</h3>
            <p>
              Historical automated data quality validation runs.
            </p>
          </div>

          <span
            className="reading-count"
            style={badgeStyle}
          >
            {validationRuns.length} runs
          </span>
        </div>

        {validationRuns.length === 0 ? (
          <div className="chart-loading">
            No validation history is available.
          </div>
        ) : (
          <div className="data-table">
            <div className="table-row table-header">
              <span>Run ID</span>
              <span>Timestamp</span>
              <span>Status</span>
              <span>Issues Found</span>
            </div>

            {validationRuns.map((run) => (
              <div
                className="table-row"
                key={run.run_id}
              >
                <strong>
                  #{run.run_id}
                </strong>

                <span>
                  {formatDateTime(run.run_timestamp)}
                </span>

                <span
                  className={`status-badge ${
                    run.validation_status === "PASSED"
                      ? "low"
                      : "high"
                  }`}
                >
                  {run.validation_status}
                </span>

                <span>
                  {run.issue_count}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>
    </>
  );
}


/* ============================================================
   SETTINGS PAGE
   ============================================================ */

function SettingsPage({
  apiConnected,
  qualitySummary,
}) {
  const latestValidation =
    qualitySummary?.latest_validation;

  const validationPassed =
    latestValidation?.validation_status === "PASSED";

  const formatDateTime = (value) => {
    if (!value) return "Not available";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
      return String(value);
    }

    return date.toLocaleString("en-US", {
      dateStyle: "medium",
      timeStyle: "short",
    });
  };

  return (
    <div className="settings-page">

      {/* PAGE HEADER */}

      <div className="page-heading settings-heading">
        <div>
          <h2>Settings</h2>
          <p>
            Platform configuration, system status and application
            readiness.
          </p>
        </div>

        <div className="period-label">
          Platform Status
        </div>
      </div>


      {/* TOP STATUS */}

      <div className="settings-status-grid">

        <div className="settings-status-card">
          <div className="settings-status-icon">
            <Server size={18} />
          </div>

          <div>
            <span>Manufacturing API</span>
            <strong>
              {apiConnected ? "Connected" : "Unavailable"}
            </strong>
          </div>

          <span
            className={`status-badge ${
              apiConnected ? "low" : "high"
            }`}
          >
            {apiConnected ? "Online" : "Offline"}
          </span>
        </div>


        <div className="settings-status-card">
          <div className="settings-status-icon">
            <Database size={18} />
          </div>

          <div>
            <span>PostgreSQL</span>
            <strong>Connected</strong>
          </div>

          <span className="status-badge low">
            Online
          </span>
        </div>


        <div className="settings-status-card">
          <div className="settings-status-icon">
            <ShieldCheck size={18} />
          </div>

          <div>
            <span>Data Validation</span>
            <strong>
              {validationPassed ? "Passed" : "Review"}
            </strong>
          </div>

          <span
            className={`status-badge ${
              validationPassed ? "low" : "medium"
            }`}
          >
            {validationPassed ? "Healthy" : "Review"}
          </span>
        </div>

      </div>


      {/* ACCOUNT + PLATFORM */}

      <div className="settings-two-column">

        <section className="panel settings-panel">

          <div className="panel-header">
            <div>
              <h3>Account</h3>
              <p>
                Current user and organization information
              </p>
            </div>
          </div>

          <div className="settings-details">

            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <User size={16} />
              </div>

              <div>
                <span>User</span>
                <strong>Business Analyst</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <ShieldCheck size={16} />
              </div>

              <div>
                <span>Role</span>
                <strong>Business Analyst</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <Factory size={16} />
              </div>

              <div>
                <span>Organization</span>
                <strong>Apex Manufacturing</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <CheckCircle2 size={16} />
              </div>

              <div>
                <span>Account Status</span>
                <strong>Active</strong>
              </div>

              <span className="status-badge low">
                Active
              </span>
            </div>

          </div>

        </section>


        <section className="panel settings-panel">

          <div className="panel-header">
            <div>
              <h3>Platform Information</h3>
              <p>
                Application and infrastructure details
              </p>
            </div>
          </div>

          <div className="settings-details">

            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <Code2 size={16} />
              </div>

              <div>
                <span>Application Version</span>
                <strong>1.0.0</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <Server size={16} />
              </div>

              <div>
                <span>Environment</span>
                <strong>Local Development</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <Database size={16} />
              </div>

              <div>
                <span>Database</span>
                <strong>PostgreSQL 17</strong>
              </div>
            </div>


            <div className="settings-detail-row">
              <div className="settings-detail-icon">
                <Activity size={16} />
              </div>

              <div>
                <span>ML Model</span>
                <strong>machine_failure_model_v1</strong>
              </div>
            </div>

          </div>

        </section>

      </div>


      {/* SYSTEM CONFIGURATION */}

      <section className="panel settings-panel full-panel">

        <div className="panel-header">
          <div>
            <h3>System Configuration</h3>
            <p>
              Current application services and data infrastructure
            </p>
          </div>
        </div>

        <div className="settings-config-grid">

          <div className="settings-config-item">

            <div className="settings-config-icon">
              <Server size={17} />
            </div>

            <div>
              <strong>Manufacturing API</strong>
              <span>
                FastAPI backend service
              </span>
            </div>

            <span
              className={`status-badge ${
                apiConnected ? "low" : "high"
              }`}
            >
              {apiConnected ? "Connected" : "Offline"}
            </span>

          </div>


          <div className="settings-config-item">

            <div className="settings-config-icon">
              <Database size={17} />
            </div>

            <div>
              <strong>PostgreSQL</strong>
              <span>
                Operational manufacturing database
              </span>
            </div>

            <span className="status-badge low">
              Connected
            </span>

          </div>


          <div className="settings-config-item">

            <div className="settings-config-icon">
              <ShieldCheck size={17} />
            </div>

            <div>
              <strong>Data Validation</strong>
              <span>
                Automated database quality validation
              </span>
            </div>

            <span
              className={`status-badge ${
                validationPassed ? "low" : "medium"
              }`}
            >
              {validationPassed ? "Passed" : "Review"}
            </span>

          </div>


          <div className="settings-config-item">

            <div className="settings-config-icon">
              <Clock3 size={17} />
            </div>

            <div>
              <strong>Last Validation</strong>
              <span>
                Most recent validation run
              </span>
            </div>

            <strong className="settings-config-value">
              {formatDateTime(
                latestValidation?.run_timestamp
              )}
            </strong>

          </div>

        </div>

      </section>


      {/* SECURITY */}

      <section className="panel settings-panel full-panel">

        <div className="panel-header">
          <div>
            <h3>Security</h3>
            <p>
              Application security capabilities and implementation
              status
            </p>
          </div>

          <span className="status-badge medium">
            Next Phase
          </span>
        </div>

        <div className="security-grid">

          <div className="security-item">

            <div className="security-item-top">
              <div className="settings-config-icon">
                <Lock size={17} />
              </div>

              <span className="status-badge medium">
                Next Phase
              </span>
            </div>

            <strong>Authentication</strong>

            <span>
              User login and session management
            </span>

          </div>


          <div className="security-item">

            <div className="security-item-top">
              <div className="settings-config-icon">
                <ShieldCheck size={17} />
              </div>

              <span className="status-badge medium">
                Next Phase
              </span>
            </div>

            <strong>Role-Based Access</strong>

            <span>
              Permission control by application role
            </span>

          </div>


          <div className="security-item">

            <div className="security-item-top">
              <div className="settings-config-icon">
                <FileText size={17} />
              </div>

              <span className="status-badge medium">
                Next Phase
              </span>
            </div>

            <strong>Audit Logging</strong>

            <span>
              Tracking security and system activities
            </span>

          </div>


          <div className="security-item">

            <div className="security-item-top">
              <div className="settings-config-icon">
                <Lock size={17} />
              </div>

              <span className="status-badge medium">
                Development
              </span>
            </div>

            <strong>API Authentication</strong>

            <span>
              API currently runs without authentication
            </span>

          </div>

        </div>

      </section>


      {/* PLATFORM READINESS */}

      <section className="panel settings-panel full-panel">

        <div className="panel-header">
          <div>
            <h3>Platform Readiness</h3>
            <p>
              Current implementation status of major platform
              capabilities
            </p>
          </div>
        </div>

        <div className="readiness-grid">

          <div className="readiness-item">
            <div className="readiness-icon">
              <Database size={17} />
            </div>

            <div>
              <span>Database</span>
              <strong>Ready</strong>
              <small>
                PostgreSQL operational database
              </small>
            </div>
          </div>


          <div className="readiness-item">
            <div className="readiness-icon">
              <ShieldCheck size={17} />
            </div>

            <div>
              <span>Data Quality</span>
              <strong>Ready</strong>
              <small>
                Validation and issue monitoring
              </small>
            </div>
          </div>


          <div className="readiness-item">
            <div className="readiness-icon">
              <BarChart3 size={17} />
            </div>

            <div>
              <span>Analytics</span>
              <strong>Ready</strong>
              <small>
                SQL analytics and API endpoints
              </small>
            </div>
          </div>


          <div className="readiness-item">
            <div className="readiness-icon">
              <Lock size={17} />
            </div>

            <div>
              <span>Security</span>
              <strong>Next Phase</strong>
              <small>
                Authentication and access control
              </small>
            </div>
          </div>

        </div>

      </section>


    </div>
  );
}

/* ============================================================
   MAIN APP
   ============================================================ */

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [kpis, setKpis] = useState(null);
  const [productionData, setProductionData] = useState([]);
  const [facilityData, setFacilityData] = useState([]);
  const [riskData, setRiskData] = useState([]);
  const [machineHealth, setMachineHealth] = useState([]);
  const [maintenanceAlerts, setMaintenanceAlerts] = useState([]);

  const [productionAnalytics, setProductionAnalytics] =
    useState(null);

  const [downtimeAnalytics, setDowntimeAnalytics] =
    useState(null);

  const [qualityAnalytics, setQualityAnalytics] =
    useState(null);

  const [machineAnalytics, setMachineAnalytics] =
    useState(null);

  const [qualitySummary, setQualitySummary] =
    useState(null);

  const [qualityIssues, setQualityIssues] =
    useState([]);

  const [validationRuns, setValidationRuns] =
    useState([]);

  const [loading, setLoading] = useState(true);

  const [analyticsLoading, setAnalyticsLoading] =
    useState(true);

  const [dataQualityLoading, setDataQualityLoading] =
    useState(true);

  const [apiError, setApiError] = useState(false);


  /* ============================================================
     DASHBOARD DATA
     ============================================================ */

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const [
          kpiResponse,
          productionResponse,
          facilityResponse,
          riskResponse,
          machineHealthResponse,
          maintenanceResponse,
        ] = await Promise.all([
          fetch(`${API_URL}/kpis`),
          fetch(`${API_URL}/production-performance`),
          fetch(`${API_URL}/facility-performance`),
          fetch(`${API_URL}/machine-risk-distribution`),
          fetch(`${API_URL}/machine-health`),
          fetch(`${API_URL}/maintenance-alerts`),
        ]);

        if (
          !kpiResponse.ok ||
          !productionResponse.ok ||
          !facilityResponse.ok ||
          !riskResponse.ok ||
          !machineHealthResponse.ok ||
          !maintenanceResponse.ok
        ) {
          throw new Error("Unable to load dashboard data");
        }

        const kpiData = await kpiResponse.json();
        const production = await productionResponse.json();
        const facilities = await facilityResponse.json();
        const risks = await riskResponse.json();
        const health = await machineHealthResponse.json();
        const maintenance = await maintenanceResponse.json();

        setKpis(kpiData);
        setProductionData(production);
        setFacilityData(facilities);

        setRiskData(
          risks.map((item) => ({
            name: `${item.risk_level} Risk`,
            value: item.count,
          }))
        );

        setMachineHealth(health);
        setMaintenanceAlerts(maintenance);

        setLoading(false);
      } catch (error) {
        console.error("Dashboard API error:", error);
        setApiError(true);
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);


  /* ============================================================
     ANALYTICS DATA
     ============================================================ */

  useEffect(() => {
    const loadAnalyticsData = async () => {
      try {
        const [
          productionResponse,
          downtimeResponse,
          qualityResponse,
          machineResponse,
        ] = await Promise.all([
          fetch(`${API_URL}/analytics/production`),
          fetch(`${API_URL}/analytics/downtime`),
          fetch(`${API_URL}/analytics/quality`),
          fetch(`${API_URL}/analytics/machines`),
        ]);

        if (
          !productionResponse.ok ||
          !downtimeResponse.ok ||
          !qualityResponse.ok ||
          !machineResponse.ok
        ) {
          throw new Error("Unable to load analytics data");
        }

        const production =
          await productionResponse.json();

        const downtime =
          await downtimeResponse.json();

        const quality =
          await qualityResponse.json();

        const machines =
          await machineResponse.json();

        setProductionAnalytics(production);
        setDowntimeAnalytics(downtime);
        setQualityAnalytics(quality);
        setMachineAnalytics(machines);

        setAnalyticsLoading(false);
      } catch (error) {
        console.error("Analytics API error:", error);
        setApiError(true);
        setAnalyticsLoading(false);
      }
    };

    loadAnalyticsData();
  }, []);


  /* ============================================================
     DATA QUALITY DATA
     ============================================================ */

  useEffect(() => {
    const loadDataQuality = async () => {
      try {
        const [
          summaryResponse,
          issuesResponse,
          validationResponse,
        ] = await Promise.all([
          fetch(`${API_URL}/data-quality/summary`),
          fetch(`${API_URL}/data-quality/issues`),
          fetch(`${API_URL}/data-quality/validation-runs`),
        ]);

        if (
          !summaryResponse.ok ||
          !issuesResponse.ok ||
          !validationResponse.ok
        ) {
          throw new Error(
            "Unable to load data quality information"
          );
        }

        const summary =
          await summaryResponse.json();

        const issues =
          await issuesResponse.json();

        const validations =
          await validationResponse.json();

        setQualitySummary(summary);
        setQualityIssues(issues);
        setValidationRuns(validations);

        setDataQualityLoading(false);
      } catch (error) {
        console.error(
          "Data Quality API error:",
          error
        );

        setApiError(true);
        setDataQualityLoading(false);
      }
    };

    loadDataQuality();
  }, []);


  const pageTitles = {
    dashboard: "Dashboard",
    production: "Production",
    machineHealth: "Machine Health",
    maintenance: "Maintenance",
    analytics: "Analytics",
    dataQuality: "Data Quality",
    settings: "Settings",
  };


  const renderPage = () => {
    if (activePage === "production") {
      return (
        <ProductionPage
          productionData={productionData}
          facilityData={facilityData}
        />
      );
    }

    if (activePage === "machineHealth") {
      return (
        <MachineHealthPage
          machineHealth={machineHealth}
        />
      );
    }

    if (activePage === "maintenance") {
      return (
        <MaintenancePage
          maintenanceAlerts={maintenanceAlerts}
        />
      );
    }

    if (activePage === "analytics") {
      return (
        <AnalyticsPage
          productionAnalytics={productionAnalytics}
          downtimeAnalytics={downtimeAnalytics}
          qualityAnalytics={qualityAnalytics}
          machineAnalytics={machineAnalytics}
          analyticsLoading={analyticsLoading}
        />
      );
    }

    if (activePage === "dataQuality") {
      return (
        <DataQualityPage
          qualitySummary={qualitySummary}
          qualityIssues={qualityIssues}
          validationRuns={validationRuns}
          dataQualityLoading={dataQualityLoading}
        />
      );
    }

    if (activePage === "settings") {
      return (
        <SettingsPage
          apiConnected={!apiError}
          qualitySummary={qualitySummary}
        />
      );
    }

    return (
      <DashboardPage
        kpis={kpis}
        productionData={productionData}
        facilityData={facilityData}
        riskData={riskData}
        maintenanceAlerts={maintenanceAlerts}
        loading={loading}
      />
    );
  };


  return (
    <div className="app">

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            <Factory size={22} />
          </div>

          <div>
            <div className="brand-name">
              Apex
            </div>

            <div className="brand-subtitle">
              Manufacturing Intelligence
            </div>
          </div>

        </div>


        <div className="nav-section">

          <div className="nav-label">
            MAIN
          </div>


          <button
            className={`nav-item ${
              activePage === "dashboard"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("dashboard")
            }
          >
            <LayoutDashboard size={18} />
            Dashboard
          </button>


          <button
            className={`nav-item ${
              activePage === "production"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("production")
            }
          >
            <Factory size={18} />
            Production
          </button>


          <button
            className={`nav-item ${
              activePage === "machineHealth"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("machineHealth")
            }
          >
            <Activity size={18} />
            Machine Health
          </button>


          <button
            className={`nav-item ${
              activePage === "maintenance"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("maintenance")
            }
          >
            <Wrench size={18} />
            Maintenance
          </button>

        </div>


        <div className="nav-section system-section">

          <div className="nav-label">
            SYSTEM
          </div>


          <button
            className={`nav-item ${
              activePage === "analytics"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("analytics")
            }
          >
            <BarChart3 size={18} />
            Analytics
          </button>


          <button
            className={`nav-item ${
              activePage === "dataQuality"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("dataQuality")
            }
          >
            <ShieldCheck size={18} />
            Data Quality
          </button>


          <button
            className={`nav-item ${
              activePage === "settings"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("settings")
            }
          >
            <Settings size={18} />
            Settings
          </button>

        </div>


        <div className="sidebar-footer">
          <Database size={16} />
          <span>
            Connected to PostgreSQL
          </span>
        </div>

      </aside>


      <main className="main-content">

        <header className="topbar">

          <div>

            <div className="breadcrumb">
              Operations / {pageTitles[activePage]}
            </div>

            <h1>
              Apex Manufacturing
            </h1>

          </div>


          <div className="user-area">

            <button className="notification-button">
              <Bell size={18} />
              <span />
            </button>


            <div className="user-profile">

              <div className="avatar">
                BA
              </div>

              <div>

                <div className="user-role">
                  Business Analyst
                </div>

                <div className="user-company">
                  Apex Manufacturing
                </div>

              </div>

            </div>

          </div>

        </header>


        <section className="dashboard-content">

          {apiError && (
            <div className="api-warning">
              <AlertTriangle size={17} />
              Unable to connect to the manufacturing API.
            </div>
          )}

          {renderPage()}

        </section>

      </main>

    </div>
  );
}


export default App;