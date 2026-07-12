import { useEffect, useState } from 'react';
import { Target, CheckSquare, Square, Zap } from 'lucide-react';
import { getJobs, getCandidates, findMatches } from '../api/endpoints';

export default function MatchingPage() {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [selectedCandidates, setSelectedCandidates] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [error, setError] = useState('');
  const [minScore, setMinScore] = useState(0.5);
  const [topK, setTopK] = useState(10);

  useEffect(() => {
    const load = async () => {
      try {
        const [jRes, cRes] = await Promise.all([getJobs(), getCandidates(1, 50)]);
        setJobs(jRes.data.jobs || []);
        setCandidates(cRes.data.candidates || []);
      } catch (err) {
        setError(
          err.response?.status === 401
            ? 'Your session has expired — please log in again.'
            : err.response?.data?.detail || 'Failed to load jobs/candidates. Is the backend running?'
        );
      }
      finally { setDataLoading(false); }
    };
    load();
  }, []);

  const toggleCandidate = (id) => {
    setSelectedCandidates(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const selectAll = () => {
    setSelectedCandidates(candidates.map(c => c.id));
  };

  const handleMatch = async () => {
    if (!selectedJob) { setError('Please select a job first.'); return; }
    if (selectedCandidates.length === 0) { setError('Please select at least one candidate.'); return; }
    setError(''); setLoading(true); setResults(null);
    try {
      const res = await findMatches(selectedJob, selectedCandidates, topK, minScore);
      setResults(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Matching failed. Try again.');
    } finally { setLoading(false); }
  };

  const scoreClass = (s) => s >= 80 ? 'score-high' : s >= 60 ? 'score-mid' : 'score-low';

  if (dataLoading) return <div className="loading-center"><div className="spinner" /></div>;

  return (
    <div>
      <div className="page-header">
        <h1>Matching Center</h1>
        <p>AI-powered candidate-to-job matching using multi-agent analysis</p>
      </div>

      <div className="grid-2" style={{ gap: 20, marginBottom: 20 }}>
        {/* Left: Config */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          <div className="card">
            <div className="section-title">1. Select Job</div>
            <div className="input-group">
              <select className="select" value={selectedJob} onChange={e => setSelectedJob(e.target.value)}>
                <option value="">— Choose a job —</option>
                {jobs.map(j => <option key={j.id} value={j.id}>{j.title}</option>)}
              </select>
            </div>
          </div>

          <div className="card">
            <div className="section-title">2. Matching Settings</div>
            <div className="form-grid">
              <div className="input-group">
                <label>Min Score (%)</label>
                <input className="input" type="number" min="0" max="100" step="5"
                  value={Math.round(minScore * 100)}
                  onChange={e => setMinScore(Number(e.target.value) / 100)}
                />
              </div>
              <div className="input-group">
                <label>Top K Results</label>
                <input className="input" type="number" min="1" max="50"
                  value={topK} onChange={e => setTopK(Number(e.target.value))}
                />
              </div>
            </div>
          </div>

          <button className="btn btn-primary" onClick={handleMatch} disabled={loading}
            style={{ justifyContent: 'center', padding: '14px' }}>
            {loading ? 'Running AI Match…' : <><Zap size={16} /> Run AI Matching</>}
          </button>
          {error && <div className="alert alert-danger">{error}</div>}
        </div>

        {/* Right: Candidate selection */}
        <div className="card">
          <div className="flex justify-between items-center" style={{ marginBottom: 12 }}>
            <div className="section-title" style={{ margin: 0 }}>
              3. Select Candidates ({selectedCandidates.length} selected)
            </div>
            <button className="btn btn-secondary btn-sm" onClick={selectAll}>Select All</button>
          </div>
          {candidates.length === 0 ? (
            <p style={{ color: 'var(--text3)', fontSize: 14 }}>No candidates found. Add candidates first.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8, maxHeight: 360, overflowY: 'auto' }}>
              {candidates.map(c => {
                const checked = selectedCandidates.includes(c.id);
                return (
                  <div
                    key={c.id}
                    onClick={() => toggleCandidate(c.id)}
                    style={{
                      display: 'flex', alignItems: 'center', gap: 12,
                      padding: '10px 12px', borderRadius: 'var(--radius-sm)',
                      cursor: 'pointer', border: '1px solid',
                      borderColor: checked ? 'var(--accent)' : 'var(--border)',
                      background: checked ? 'rgba(108,99,255,0.08)' : 'var(--bg3)',
                      transition: 'all 0.12s',
                    }}
                  >
                    {checked ? <CheckSquare size={16} style={{ color: 'var(--accent)', flexShrink: 0 }} />
                      : <Square size={16} style={{ color: 'var(--text3)', flexShrink: 0 }} />}
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontWeight: 600, fontSize: 14 }}>{c.first_name} {c.last_name}</div>
                      <div style={{ fontSize: 12, color: 'var(--text3)' }}>{c.location || 'No location'}</div>
                    </div>
                    {(() => { let sk = c.extracted_skills || []; if (typeof sk === "string") sk = sk.split(",").map(s => s.trim()).filter(Boolean); if (!Array.isArray(sk)) sk = []; return sk.slice(0, 2).map(s => <span key={s} className="tag" style={{ fontSize: 11 }}>{s}</span>); })()}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Results */}
      {results && (
        <div className="card">
          <div className="flex justify-between items-center" style={{ marginBottom: 20 }}>
            <div>
              <div className="section-title" style={{ margin: 0 }}>Match Results</div>
              <p style={{ color: 'var(--text2)', fontSize: 13, marginTop: 4 }}>
                {results.total_matches} candidates matched above {Math.round(minScore * 100)}% threshold
              </p>
            </div>
            <span className="badge badge-teal"><Target size={12} /> {results.total_matches} Matches</span>
          </div>

          {results.matches?.length === 0 ? (
            <div className="empty-state" style={{ padding: '30px' }}>
              <Target size={32} />
              <h3>No matches found</h3>
              <p>Try lowering the minimum score or selecting more candidates.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {results.matches?.map((m, i) => (
                <div key={m.candidate_id} style={{
                  display: 'flex', alignItems: 'center', gap: 16,
                  padding: '16px', borderRadius: 'var(--radius-sm)',
                  background: 'var(--bg3)', border: '1px solid var(--border)',
                }}>
                  <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 18, fontWeight: 700, color: 'var(--text3)', minWidth: 28 }}>
                    #{i + 1}
                  </div>
                  <div className={`score-ring ${scoreClass(m.match_score)}`}>
                    {m.match_score}
                  </div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 700, fontSize: 15 }}>{m.candidate_name}</div>
                    <div className="flex gap-2 mt-1 flex-wrap">
                      {(m.strengths || []).map(s => (
                        <span key={s} className="badge badge-teal" style={{ fontSize: 11 }}>✓ {s}</span>
                      ))}
                      {(m.gaps || []).map(g => (
                        <span key={g} className="badge badge-red" style={{ fontSize: 11 }}>✗ {g}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
