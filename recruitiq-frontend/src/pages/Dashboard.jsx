import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Users,
  Briefcase,
  Target,
  TrendingUp,
  ArrowRight,
  Sparkles,
  GraduationCap,
  Scale,
} from 'lucide-react';

import {
  getCandidates,
  getJobs,
  getHiringFunnel,
  getSkillGapAnalytics,
  getBiasAudit,
} from '../api/endpoints';

import { useAuth } from '../AuthContext';

export default function Dashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [stats, setStats] = useState({
    candidates: 0,
    jobs: 0,
    funnel: null,
  });

  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [
          cRes,
          jRes,
          fRes,
        ] = await Promise.all([
          getCandidates(1, 1),
          getJobs(),
          getHiringFunnel(),
        ]);

        setStats({
          candidates:
            cRes.data.total || 0,

          jobs:
            jRes.data.total ||
            jRes.data.jobs?.length ||
            0,

          funnel: fRes.data,
        });
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    load();

    // Best-effort AI suggestions — independent of the main stats load so a
    // slow/empty analytics dataset never blocks the core dashboard.
    const loadSuggestions = async () => {
      const items = [];
      try {
        const gapRes = await getSkillGapAnalytics();
        const topGap = gapRes.data?.top_skill_gaps?.[0];
        if (topGap) {
          items.push({
            icon: GraduationCap,
            title: `"${topGap[0]}" is your top skill gap`,
            desc: `${topGap[1]} candidate${topGap[1] > 1 ? 's' : ''} are missing this skill across your pipeline. See the Insights Hub for the full breakdown.`,
            to: '/insights',
          });
        }
      } catch { /* analytics may be empty on a fresh install — skip silently */ }

      try {
        const biasRes = await getBiasAudit();
        const rec = biasRes.data?.recommendations?.[0];
        if (rec) {
          items.push({
            icon: Scale,
            title: 'Diversity recommendation',
            desc: rec,
            to: '/insights',
          });
        }
      } catch { /* same as above */ }

      setSuggestions(items);
    };

    loadSuggestions();
  }, []);

  const funnel = stats.funnel || {};

  const hour = new Date().getHours();

  let greeting = 'Good Morning';

  if (hour >= 12 && hour < 17) {
    greeting = 'Good Afternoon';
  } else if (hour >= 17) {
    greeting = 'Good Evening';
  }

  const userName =
    user?.full_name ||
    user?.name ||
    'Recruiter';

  const quickLinks = [
    {
      label: 'Add Candidate',
      to: '/candidates',
      icon: Users,
      color: 'purple',
    },
    {
      label: 'Post a Job',
      to: '/jobs',
      icon: Briefcase,
      color: 'teal',
    },
    {
      label: 'Run Matching',
      to: '/matching',
      icon: Target,
      color: 'orange',
    },
    {
      label: 'View Analytics',
      to: '/analytics',
      icon: TrendingUp,
      color: 'red',
    },
  ];

  if (loading) {
    return (
      <div className="loading-center">
        <div className="spinner" />
      </div>
    );
  }

  return (
    <div>
      <div className="hero-banner">
        <h1>
          {greeting}, {userName} 👋
        </h1>

        <p>
          Here's what's happening in your recruitment pipeline today.
        </p>
      </div>

      <div
        className="grid-4"
        style={{
          marginBottom: 24,
        }}
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
            <Target size={20} />
          </div>

          <div>
            <div className="stat-value">
              {funnel.shortlisted || 0}
            </div>

            <div className="stat-label">
              Shortlisted
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon orange">
            <TrendingUp size={20} />
          </div>

          <div>
            <div className="stat-value">
              {funnel.strong_hire || 0}
            </div>

            <div className="stat-label">
              Strong Hires
            </div>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon red">
            <Briefcase size={20} />
          </div>

          <div>
            <div className="stat-value">
              {stats.jobs}
            </div>

            <div className="stat-label">
              Active Jobs
            </div>
          </div>
        </div>
      </div>

      <div
        className="grid-2"
        style={{
          gap: 20,
        }}
      >
        <div className="card">
          <div className="section-title">
            Hiring Decisions
          </div>

          {[
            {
              label: 'Strong Hire',
              value: funnel.strong_hire || 0,
            },
            {
              label: 'Hire',
              value: funnel.hire || 0,
            },
            {
              label: 'Consider',
              value: funnel.consider || 0,
            },
            {
              label: 'Reject',
              value: funnel.reject || 0,
            },
          ].map((item) => {
            const total =
              funnel.total_candidates || 1;

            const pct = Math.round(
              (item.value / total) * 100
            );

            return (
              <div
                key={item.label}
                style={{
                  marginBottom: 16,
                }}
              >
                <div
                  className="flex justify-between items-center"
                  style={{
                    marginBottom: 6,
                  }}
                >
                  <span>{item.label}</span>

                  <span>{item.value}</span>
                </div>

                <div className="progress-bar-wrap">
                  <div
                    className="progress-bar"
                    style={{
                      width: `${pct}%`,
                    }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <div className="card">
          <div className="section-title">
            Quick Actions
          </div>

          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: 10,
            }}
          >
            {quickLinks.map(
              ({
                label,
                to,
                icon: Icon,
                color,
              }) => (
                <button
                  key={to}
                  className="btn btn-secondary"
                  onClick={() =>
                    navigate(to)
                  }
                  style={{
                    justifyContent:
                      'space-between',
                    padding: '14px 16px',
                  }}
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`stat-icon ${color}`}
                      style={{
                        width: 34,
                        height: 34,
                        borderRadius: 8,
                      }}
                    >
                      <Icon size={16} />
                    </div>

                    <span>{label}</span>
                  </div>

                  <ArrowRight
                    size={16}
                    style={{
                      color:
                        'var(--text3)',
                    }}
                  />
                </button>
              )
            )}
          </div>
        </div>
      </div>

      {suggestions.length > 0 && (
        <div className="card" style={{ marginTop: 20 }}>
          <div className="section-title">
            <Sparkles size={15} style={{ verticalAlign: -3, marginRight: 6 }} />
            AI Suggestions
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {suggestions.map((s, i) => (
              <button
                key={i}
                className="suggestion-card"
                style={{ width: '100%', textAlign: 'left', cursor: 'pointer', border: '1px solid var(--border)', font: 'inherit' }}
                onClick={() => navigate(s.to)}
              >
                <div className="suggestion-icon"><s.icon size={17} /></div>
                <div>
                  <div className="suggestion-title">{s.title}</div>
                  <div className="suggestion-desc">{s.desc}</div>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}