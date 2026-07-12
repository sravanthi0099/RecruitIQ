import { useEffect, useState } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  PieChart, Pie, Legend,
} from 'recharts';
import {
  Gauge, Scale, IndianRupee, GraduationCap, ListChecks,
  Sparkles, MapPin, TrendingUp, Trophy,
} from 'lucide-react';
import {
  getRecruiterDashboard, getBiasAudit, getSalaryIntelligence,
  getSkillGapAnalytics, getShortlist, getJobs,
} from '../api/endpoints';

const COLORS = ['#6c63ff', '#00d4aa', '#f5a623', '#ff6584', '#5b52f6', '#0d9e94'];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 8, padding: '10px 14px', fontSize: 13 }}>
        <div style={{ fontWeight: 700, marginBottom: 4 }}>{label}</div>
        {payload.map((p) => (
          <div key={p.dataKey} style={{ color: p.fill || 'var(--accent2)' }}>
            {p.name || p.dataKey}: <strong>{p.value}</strong>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const TABS = [
  { key: 'recruiter', label: 'Recruiter Dashboard', icon: Gauge },
  { key: 'bias', label: 'Bias Audit', icon: Scale },
  { key: 'salary', label: 'Salary Intelligence', icon: IndianRupee },
  { key: 'skillgap', label: 'Skill Gap', icon: GraduationCap },
  { key: 'shortlist', label: 'Shortlist', icon: ListChecks },
];

function SuggestionCard({ icon: Icon, title, desc }) {
  return (
    <div className="suggestion-card">
      <div className="suggestion-icon"><Icon size={17} /></div>
      <div>
        <div className="suggestion-title">{title}</div>
        <div className="suggestion-desc">{desc}</div>
      </div>
    </div>
  );
}

export default function InsightsPage() {
  const [tab, setTab] = useState('recruiter');

  return (
    <div>
      <div className="page-header">
        <h1>Insights</h1>
        <p>Bias auditing, salary intelligence, skill-gap trends, and recruiter-level shortlisting — all AI-derived from your live pipeline.</p>
      </div>

      <div className="tabs">
        {TABS.map(({ key, label, icon: Icon }) => (
          <button key={key} className={`tab ${tab === key ? 'active' : ''}`} onClick={() => setTab(key)}>
            <span className="flex items-center gap-2"><Icon size={14} /> {label}</span>
          </button>
        ))}
      </div>

      {tab === 'recruiter' && <RecruiterDashboardTab />}
      {tab === 'bias' && <BiasAuditTab />}
      {tab === 'salary' && <SalaryIntelligenceTab />}
      {tab === 'skillgap' && <SkillGapTab />}
      {tab === 'shortlist' && <ShortlistTab />}
    </div>
  );
}

/* ============================================================
   1. RECRUITER DASHBOARD
   ============================================================ */
function RecruiterDashboardTab() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    getRecruiterDashboard()
      .then((res) => alive && setData(res.data))
      .catch(() => alive && setData(null))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  if (loading) return <div className="loading-center"><div className="spinner" /></div>;
  if (!data) return <div className="empty-state"><Gauge size={40} /><h3>No data yet</h3><p>Run some candidates through Full Analysis to populate this dashboard.</p></div>;

  const decisionData = [
    { name: 'Strong Hire', count: data.strong_hire || 0 },
    { name: 'Hire', count: data.hire || 0 },
    { name: 'Consider', count: data.consider || 0 },
    { name: 'Reject', count: data.reject || 0 },
  ];

  const rejectRate = data.total_candidates > 0 ? Math.round((data.reject / data.total_candidates) * 100) : 0;

  return (
    <div>
      <div className="grid-4" style={{ marginBottom: 20 }}>
        <div className="stat-card">
          <div className="stat-icon purple"><Gauge size={20} /></div>
          <div><div className="stat-value">{data.total_candidates || 0}</div><div className="stat-label">Total Evaluated</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon teal"><Trophy size={20} /></div>
          <div><div className="stat-value">{data.strong_hire || 0}</div><div className="stat-label">Strong Hires</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon orange"><TrendingUp size={20} /></div>
          <div><div className="stat-value">{data.hire || 0}</div><div className="stat-label">Hires</div></div>
        </div>
        <div className="stat-card">
          <div className="stat-icon red"><Scale size={20} /></div>
          <div><div className="stat-value">{rejectRate}%</div><div className="stat-label">Reject Rate</div></div>
        </div>
      </div>

      <div className="grid-2" style={{ gap: 20, marginBottom: 20 }}>
        <div className="card">
          <div className="section-title">Decision Breakdown</div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={decisionData}>
              <XAxis dataKey="name" tick={{ fontSize: 12 }} />
              <YAxis allowDecimals={false} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[6, 6, 0, 0]} isAnimationActive animationDuration={700}>
                {decisionData.map((d, i) => <Cell key={d.name} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <div className="section-title">Top Candidates</div>
          {(!data.top_candidates || data.top_candidates.length === 0) ? (
            <p style={{ color: 'var(--text3)', fontSize: 14 }}>No ranked candidates yet.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 10, maxHeight: 260, overflowY: 'auto' }}>
              {data.top_candidates.map((c, i) => (
                <div key={c.candidate_id} className="flex items-center gap-3" style={{ padding: '8px 10px', borderRadius: 'var(--radius-sm)', background: 'var(--bg3)' }}>
                  <span style={{ fontFamily: "'Space Mono', monospace", color: 'var(--text3)', fontWeight: 700, minWidth: 22 }}>#{i + 1}</span>
                  <span style={{ flex: 1, fontSize: 13.5 }} className="font-mono">{c.candidate_id.slice(0, 8)}…</span>
                  <span className="badge badge-teal">{c.score}</span>
                  <span className="badge badge-purple">{c.decision || 'Pending'}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <div className="section-title"><Sparkles size={15} style={{ verticalAlign: -3, marginRight: 6 }} />Suggestions</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {rejectRate > 50 && (
            <SuggestionCard icon={Scale} title="High reject rate detected"
              desc={`${rejectRate}% of evaluated candidates were rejected. Consider revisiting your job description's required skills or sourcing channels.`} />
          )}
          {data.strong_hire > 0 && (
            <SuggestionCard icon={Trophy} title="Fast-track your strong hires"
              desc={`You have ${data.strong_hire} Strong Hire candidate${data.strong_hire > 1 ? 's' : ''} — send interview invites before they accept other offers.`} />
          )}
          {(!data.total_candidates || data.total_candidates === 0) && (
            <SuggestionCard icon={Sparkles} title="No data yet"
              desc="Run Full Analysis on a few candidates to unlock personalized hiring suggestions here." />
          )}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   2. BIAS AUDIT
   ============================================================ */
function BiasAuditTab() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    getBiasAudit()
      .then((res) => alive && setData(res.data))
      .catch(() => alive && setData(null))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  if (loading) return <div className="loading-center"><div className="spinner" /></div>;
  if (!data) return <div className="empty-state"><Scale size={40} /><h3>No bias data</h3><p>Add candidates with location data to see geographic diversity.</p></div>;

  const geoData = Object.entries(data.geographic_diversity || {}).map(([location, pct]) => ({
    location, pct: Math.round(pct * 100),
  }));

  return (
    <div>
      <div className="grid-2" style={{ gap: 20, marginBottom: 20 }}>
        <div className="card">
          <div className="section-title"><MapPin size={15} style={{ verticalAlign: -3, marginRight: 6 }} />Geographic Diversity</div>
          {geoData.length === 0 ? (
            <p style={{ color: 'var(--text3)', fontSize: 14 }}>No location data available yet.</p>
          ) : (
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie data={geoData} dataKey="pct" nameKey="location" outerRadius={100} innerRadius={50} isAnimationActive animationDuration={700}>
                  {geoData.map((entry, i) => <Cell key={entry.location} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip formatter={(v) => `${v}%`} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="card">
          <div className="section-title">Bias Score</div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginTop: 10 }}>
            <div className={`score-ring ${data.bias_score < 0.3 ? 'score-high' : data.bias_score < 0.6 ? 'score-mid' : 'score-low'}`} style={{ width: 72, height: 72, fontSize: 20 }}>
              {Math.round((data.bias_score || 0) * 100)}
            </div>
            <div style={{ fontSize: 13.5, color: 'var(--text2)' }}>
              Lower is better — this score reflects imbalance across gender, education, and geographic signals currently tracked.
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="section-title"><Sparkles size={15} style={{ verticalAlign: -3, marginRight: 6 }} />Recommendations</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {(data.recommendations || []).map((rec, i) => (
            <SuggestionCard key={i} icon={Scale} title="Diversity recommendation" desc={rec} />
          ))}
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   3. SALARY INTELLIGENCE
   ============================================================ */
function SalaryIntelligenceTab() {
  const [jobTitle, setJobTitle] = useState('');
  const [location, setLocation] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fmtINR = (n) => `₹${(n / 100000).toFixed(1)}L`;

  const handleEstimate = async () => {
    setLoading(true); setError(''); setData(null);
    try {
      const res = await getSalaryIntelligence(jobTitle || undefined, location || undefined);
      setData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Could not fetch salary intelligence.');
    } finally { setLoading(false); }
  };

  const chartData = data ? [
    { name: 'P25', value: data.percentiles.p25 },
    { name: 'Median', value: data.percentiles.p50 },
    { name: 'P75', value: data.percentiles.p75 },
  ] : [];

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="section-title">Estimate Market Salary</div>
        <div className="form-grid">
          <div className="input-group">
            <label>Job Title</label>
            <input className="input" placeholder="e.g. AI Engineer" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} />
          </div>
          <div className="input-group">
            <label>Location (optional)</label>
            <input className="input" placeholder="e.g. Hyderabad" value={location} onChange={(e) => setLocation(e.target.value)} />
          </div>
        </div>
        <button className="btn btn-primary animated-btn" style={{ marginTop: 16 }} onClick={handleEstimate} disabled={loading}>
          {loading ? 'Estimating…' : <><IndianRupee size={15} /> Get Salary Intelligence</>}
        </button>
        {error && <div className="alert alert-danger" style={{ marginTop: 14 }}>{error}</div>}
      </div>

      {data && (
        <div className="grid-2" style={{ gap: 20 }}>
          <div className="card">
            <div className="section-title">Percentile Breakdown</div>
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={chartData}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis tickFormatter={fmtINR} width={60} />
                <Tooltip formatter={(v) => fmtINR(v)} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]} fill="#6c63ff" isAnimationActive animationDuration={700} />
              </BarChart>
            </ResponsiveContainer>
          </div>
          <div className="card">
            <div className="section-title">Market Range</div>
            <div style={{ fontSize: 28, fontWeight: 700, fontFamily: "'Space Mono', monospace", color: 'var(--accent2)', marginBottom: 6 }}>
              {fmtINR(data.market_salary.min)} – {fmtINR(data.market_salary.max)}
            </div>
            <div style={{ fontSize: 13.5, color: 'var(--text2)', marginBottom: 16 }}>
              Average: <strong>{fmtINR(data.market_salary.average)}</strong> per annum ({data.currency})
            </div>
            <SuggestionCard icon={Sparkles} title="Negotiation tip"
              desc={`Anchor initial offers near the P25–P50 band (${fmtINR(data.percentiles.p25)}–${fmtINR(data.percentiles.p50)}) and reserve headroom up to ${fmtINR(data.percentiles.p75)} for strong closers.`} />
          </div>
        </div>
      )}
    </div>
  );
}

/* ============================================================
   4. SKILL GAP
   ============================================================ */
function SkillGapTab() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    getSkillGapAnalytics()
      .then((res) => alive && setData(res.data))
      .catch(() => alive && setData(null))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, []);

  if (loading) return <div className="loading-center"><div className="spinner" /></div>;
  if (!data || !data.top_skill_gaps?.length) {
    return <div className="empty-state"><GraduationCap size={40} /><h3>No skill-gap data yet</h3><p>Run Full Analysis on candidates to surface the most common missing skills.</p></div>;
  }

  const chartData = data.top_skill_gaps.map(([skill, count]) => ({ skill, count }));
  const topGap = chartData[0];

  return (
    <div>
      <div className="grid-2" style={{ gap: 20, marginBottom: 20 }}>
        <div className="card" style={{ gridColumn: '1 / -1' }}>
          <div className="section-title">Most Common Missing Skills</div>
          <ResponsiveContainer width="100%" height={Math.max(240, chartData.length * 34)}>
            <BarChart data={chartData} layout="vertical" margin={{ left: 20 }}>
              <XAxis type="number" allowDecimals={false} />
              <YAxis type="category" dataKey="skill" width={120} tick={{ fontSize: 12.5 }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="count" radius={[0, 6, 6, 0]} isAnimationActive animationDuration={700}>
                {chartData.map((d, i) => <Cell key={d.skill} fill={COLORS[i % COLORS.length]} />)}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="card">
        <div className="section-title"><Sparkles size={15} style={{ verticalAlign: -3, marginRight: 6 }} />Suggestions</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          <SuggestionCard icon={GraduationCap} title={`"${topGap.skill}" is your biggest gap`}
            desc={`${topGap.count} candidate${topGap.count > 1 ? 's' : ''} are missing this skill. Consider a targeted upskilling track, or widen sourcing to candidates already strong in ${topGap.skill}.`} />
          <SuggestionCard icon={Sparkles} title="Total gaps tracked" desc={`${data.total_missing_skills} missing-skill mentions found across all evaluated candidates.`} />
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   5. SHORTLIST
   ============================================================ */
function ShortlistTab() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getJobs().then((res) => setJobs(res.data.jobs || [])).catch(() => {}).finally(() => setDataLoading(false));
  }, []);

  const handleFetch = async () => {
    if (!selectedJob) { setError('Select a job first.'); return; }
    setError(''); setLoading(true); setData(null);
    try {
      const res = await getShortlist(selectedJob);
      if (res.data.error) { setError(res.data.error); return; }
      setData(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to build shortlist.');
    } finally { setLoading(false); }
  };

  const scoreClass = (s) => s >= 80 ? 'score-high' : s >= 60 ? 'score-mid' : 'score-low';

  if (dataLoading) return <div className="loading-center"><div className="spinner" /></div>;

  return (
    <div>
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="section-title">Build Shortlist for a Job</div>
        <div className="flex gap-2" style={{ alignItems: 'flex-end', flexWrap: 'wrap' }}>
          <div className="input-group" style={{ minWidth: 240 }}>
            <label>Job</label>
            <select className="select" value={selectedJob} onChange={(e) => setSelectedJob(e.target.value)}>
              <option value="">— Choose a job —</option>
              {jobs.map((j) => <option key={j.id} value={j.id}>{j.title}</option>)}
            </select>
          </div>
          <button className="btn btn-primary animated-btn" onClick={handleFetch} disabled={loading}>
            {loading ? 'Ranking candidates…' : <><ListChecks size={15} /> Generate Shortlist</>}
          </button>
        </div>
        {error && <div className="alert alert-danger" style={{ marginTop: 14 }}>{error}</div>}
      </div>

      {data && (
        <div className="card">
          <div className="flex justify-between items-center" style={{ marginBottom: 16 }}>
            <div className="section-title" style={{ margin: 0 }}>{data.job_title}</div>
            <span className="badge badge-teal">{data.ranked_candidates} / {data.total_candidates} ranked</span>
          </div>
          {(!data.top_candidates || data.top_candidates.length === 0) ? (
            <div className="empty-state" style={{ padding: 30 }}>
              <ListChecks size={32} /><h3>No candidates ranked</h3><p>Add candidates before generating a shortlist.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {data.top_candidates.map((c, i) => (
                <div key={c.candidate_id} style={{ display: 'flex', alignItems: 'center', gap: 16, padding: 16, borderRadius: 'var(--radius-sm)', background: 'var(--bg3)', border: '1px solid var(--border)' }}>
                  <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 18, fontWeight: 700, color: 'var(--text3)', minWidth: 28 }}>#{i + 1}</div>
                  <div className={`score-ring ${scoreClass(c.overall_score)}`}>{c.overall_score}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, fontSize: 15 }}>{c.candidate_name}</div>
                    <div style={{ fontSize: 12.5, color: 'var(--text3)', marginBottom: 6 }}>{c.email}</div>
                    <div className="flex gap-2 flex-wrap">
                      {(c.matching_skills || []).slice(0, 4).map((s) => <span key={s} className="badge badge-teal" style={{ fontSize: 11 }}>✓ {s}</span>)}
                      {(c.skill_gaps || []).slice(0, 3).map((s) => <span key={s} className="badge badge-red" style={{ fontSize: 11 }}>✗ {s}</span>)}
                    </div>
                  </div>
                  <span className="badge badge-purple">{c.recommendation}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
