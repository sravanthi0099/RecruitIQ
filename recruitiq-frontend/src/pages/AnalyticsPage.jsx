import { useEffect, useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
  Legend
} from 'recharts';

import {
  BarChart2,
  TrendingUp,
  Users,
  Percent
} from 'lucide-react';

import { getHiringFunnel } from '../api/endpoints';

const STAGE_COLORS = {
  shortlisted: '#6c63ff',
  strong_hire: '#00d4aa',
  hire: '#f5a623',
  consider: '#ff6584',
  reject: '#ff4d6d',
};

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div
        style={{
          background: 'var(--bg2)',
          border: '1px solid var(--border)',
          borderRadius: 8,
          padding: '10px 14px',
          fontSize: 13,
        }}
      >
        <div
          style={{
            fontWeight: 700,
            marginBottom: 4,
            textTransform: 'capitalize',
          }}
        >
          {label}
        </div>

        <div style={{ color: 'var(--accent2)' }}>
          Count: <strong>{payload[0].value}</strong>
        </div>
      </div>
    );
  }

  return null;
};

export default function AnalyticsPage() {
  const [funnel, setFunnel] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await getHiringFunnel();
        setFunnel(res.data);
      } catch {
        setFunnel(null);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  if (loading) {
    return (
      <div className="loading-center">
        <div className="spinner" />
      </div>
    );
  }

  if (!funnel) {
    return (
      <div className="empty-state">
        <BarChart2 size={40} />
        <h3>No analytics data</h3>
        <p>
          Add candidates and run them through the
          pipeline to see analytics.
        </p>
      </div>
    );
  }

  const statuses = {
    shortlisted: funnel.shortlisted || 0,
    strong_hire: funnel.strong_hire || 0,
    hire: funnel.hire || 0,
    consider: funnel.consider || 0,
    reject: funnel.reject || 0,
  };

  const barData = Object.entries(statuses).map(
    ([stage, count]) => ({
      stage,
      count,
    })
  );

  const pieData = barData.filter(
    (item) => item.count > 0
  );

  const convRates =
    funnel.conversion_rates || {};

  return (
    <div>
      <div className="page-header">
        <h1>Analytics</h1>
        <p>
          Recruitment funnel and pipeline
          performance
        </p>
      </div>

      {/* Stat Cards */}

      <div
        className="grid-4"
        style={{ marginBottom: 24 }}
      >
        <div className="stat-card">
          <div className="stat-icon purple">
            <Users size={20} />
          </div>

          <div>
            <div className="stat-value">
              {funnel.total_candidates || 0}
            </div>

            <div className="stat-label">
              Total Candidates
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon teal">
            <TrendingUp size={20} />
          </div>

          <div>
            <div className="stat-value">
              {statuses.shortlisted}
            </div>

            <div className="stat-label">
              Shortlisted
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon orange">
            <BarChart2 size={20} />
          </div>

          <div>
            <div className="stat-value">
              {statuses.strong_hire}
            </div>

            <div className="stat-label">
              Strong Hires
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon red">
            <Percent size={20} />
          </div>

          <div>
            <div className="stat-value">
              {funnel.total_candidates > 0
                ? `${Math.round(
                    (statuses.strong_hire /
                      funnel.total_candidates) *
                      100
                  )}%`
                : '0%'}
            </div>

            <div className="stat-label">
              Strong Hire Rate
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}

      <div
        className="grid-2"
        style={{
          gap: 20,
          marginBottom: 20,
        }}
      >
        <div className="card">
          <div className="section-title">
            Pipeline Funnel
          </div>

          <ResponsiveContainer
            width="100%"
            height={280}
          >
            <BarChart data={barData}>
              <XAxis dataKey="stage" />
              <YAxis />
              <Tooltip
                content={<CustomTooltip />}
              />

              <Bar
                dataKey="count"
                radius={[6, 6, 0, 0]}
              >
                {barData.map((entry) => (
                  <Cell
                    key={entry.stage}
                    fill={
                      STAGE_COLORS[
                        entry.stage
                      ] || '#6c63ff'
                    }
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="section-title">
            Status Distribution
          </div>

          <ResponsiveContainer
            width="100%"
            height={280}
          >
            <PieChart>
              <Pie
                data={pieData}
                dataKey="count"
                nameKey="stage"
                outerRadius={100}
                innerRadius={50}
              >
                {pieData.map((entry) => (
                  <Cell
                    key={entry.stage}
                    fill={
                      STAGE_COLORS[
                        entry.stage
                      ] || '#6c63ff'
                    }
                  />
                ))}
              </Pie>

              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Conversion Rates */}

      {Object.keys(convRates).length >
        0 && (
        <div className="card">
          <div className="section-title">
            Conversion Rates
          </div>

          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 14,
            }}
          >
            {Object.entries(
              convRates
            ).map(([stage, rate]) => {
              const pct =
                typeof rate === 'number'
                  ? Math.round(rate * 100)
                  : rate;

              return (
                <div key={stage}>
                  <div
                    className="flex justify-between items-center"
                    style={{
                      marginBottom: 6,
                    }}
                  >
                    <span>
                      {stage.replace(
                        /_/g,
                        ' → '
                      )}
                    </span>

                    <span>
                      {pct}%
                    </span>
                  </div>

                  <div className="progress-bar-wrap">
                    <div
                      className="progress-bar"
                      style={{
                        width: `${Math.min(
                          pct,
                          100
                        )}%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}