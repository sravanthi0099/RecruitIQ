import { useEffect, useState } from 'react';
import { FlaskConical, Play, ChevronDown, ChevronRight } from 'lucide-react';
import { getJobs, getCandidates, runAnalysis, getAnalysis } from '../api/endpoints';

function Section({ title, data }) {
  const [open, setOpen] = useState(true);
  if (!data || Object.keys(data).length === 0) return null;
  return (
    <div style={{ marginBottom: 12, border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', overflow: 'hidden' }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: '100%', padding: '12px 16px', background: 'var(--bg3)',
          border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 8,
          color: 'var(--text)', fontWeight: 600, fontSize: 14,
        }}
      >
        {open ? <ChevronDown size={15} /> : <ChevronRight size={15} />}
        {title}
      </button>
      {open && (
        <div style={{ padding: '16px', background: 'var(--bg)' }}>
          <pre style={{
            fontSize: 12, fontFamily: "'Space Mono', monospace",
            color: 'var(--text2)', whiteSpace: 'pre-wrap', wordBreak: 'break-word',
            lineHeight: 1.7, margin: 0,
          }}>
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default function AnalysisPage() {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [selectedCandidate, setSelectedCandidate] = useState('');
  const [analysisId, setAnalysisId] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState('');
  const [dataLoading, setDataLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      try {
        const [jRes, cRes] = await Promise.all([getJobs(), getCandidates(1, 50)]);
        setJobs(jRes.data.jobs || []);
        setCandidates(cRes.data.candidates || []);
      } catch { /* ignore */ }
      finally { setDataLoading(false); }
    };
    load();
  }, []);

  const handleRun = async () => {
  if (!selectedCandidate || !selectedJob) {
    setError('Select both a candidate and a job.');
    return;
  }

  setError('');
  setLoading(true);
  setResult(null);

  try {
    const res = await runAnalysis(
      selectedCandidate,
      selectedJob
    );

    setAnalysisId(
      res.data.analysis_id
    );

    setResult(
      res.data
    );

  } catch (err) {

    setError(
      err.response?.data?.detail ||
      'Failed to run analysis'
    );

  } finally {
    setLoading(false);
  }
};

  const handleFetch = async () => {
    if (!analysisId.trim()) { setError('Enter an analysis ID.'); return; }
    setError(''); setFetching(true);
    try {
      const res = await getAnalysis(analysisId.trim());
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis not found. Check the ID.');
    } finally { setFetching(false); }
  };

  if (dataLoading) return <div className="loading-center"><div className="spinner" /></div>;

  const genericSections = result
  ? [
      {
        key: 'resume_analysis',
        label: 'Resume Analysis'
      },
      {
        key: 'job_analysis',
        label: 'Job Analysis'
      },
      {
        key: 'skill_gap_analysis',
        label: 'Skill Gap Analysis'
      },
      {
        key: 'candidate_ranking',
        label: 'Candidate Ranking'
      },
    ]
  : [];

  return (
    <div>
      <div className="page-header">
        <h1>Full Analysis</h1>
        <p>Run deep multi-agent analysis on a candidate-job pair</p>
      </div>

      <div className="grid-2" style={{ gap: 20, marginBottom: 20 }}>
        <div className="card">
          <div className="section-title">Run New Analysis</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div className="input-group">
              <label>Select Candidate</label>
              <select className="select" value={selectedCandidate} onChange={e => setSelectedCandidate(e.target.value)}>
                <option value="">— Choose candidate —</option>
                {candidates.map(c => <option key={c.id} value={c.id}>{c.first_name} {c.last_name}</option>)}
              </select>
            </div>
            <div className="input-group">
              <label>Select Job</label>
              <select className="select" value={selectedJob} onChange={e => setSelectedJob(e.target.value)}>
                <option value="">— Choose job —</option>
                {jobs.map(j => <option key={j.id} value={j.id}>{j.title}</option>)}
              </select>
            </div>
            <button className="btn btn-primary" onClick={handleRun} disabled={loading}
              style={{ justifyContent: 'center', padding: '12px' }}>
              {loading ? 'Running Analysis…' : <><Play size={15} /> Run Full Analysis</>}
            </button>
          </div>
        </div>

        <div className="card">
          <div className="section-title">Fetch Existing Analysis</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div className="input-group">
              <label>Analysis ID</label>
              <input className="input" placeholder="Paste analysis UUID here…"
                value={analysisId} onChange={e => setAnalysisId(e.target.value)} />
            </div>
            <button className="btn btn-secondary" onClick={handleFetch} disabled={fetching}
              style={{ justifyContent: 'center', padding: '12px' }}>
              {fetching ? 'Fetching…' : <><FlaskConical size={15} /> Fetch Results</>}
            </button>
          </div>
        </div>
      </div>

      {error && <div className="alert alert-danger" style={{ marginBottom: 20 }}>{error}</div>}

      {result && (
  <div className="card">
    <div className="section-title">
      Analysis Results
    </div>

    <div
      style={{
        marginBottom: 20,
        padding: '12px',
        background: 'var(--bg3)',
        borderRadius: '8px',
      }}
    >
      <strong>Analysis ID:</strong>{" "}
      {result.analysis_id}
    </div>

    <div
      style={{
        marginBottom: 20,
        padding: '16px',
        borderRadius: '8px',
        background: '#0f172a',
        border: '1px solid var(--accent)',
      }}
    >
      <h3
        style={{
          marginBottom: 8
        }}
      >
        Final Decision
      </h3>

      <div
        style={{
          fontSize: '24px',
          fontWeight: 'bold',
          color: '#00d4aa',
        }}
      >
        {result.final_decision}
      </div>
    </div>

          {/* Interview Questions */}
          {result.interview_questions?.questions?.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 10, color: 'var(--accent)' }}>
                Interview Questions ({result.interview_questions.questions.length})
              </div>
              {result.interview_questions.questions.map((q, i) => (
                <div key={i} style={{
                  padding: '12px 14px', background: 'var(--bg3)',
                  borderRadius: 'var(--radius-sm)', marginBottom: 8, fontSize: 14,
                  borderLeft: '3px solid var(--accent)',
                }}>
                  <strong style={{ color: 'var(--text2)', fontSize: 12 }}>Q{i + 1}:</strong> {typeof q === 'string' ? q : q.question}
                </div>
              ))}
              <hr className="divider" />

            </div>
          )}

          {genericSections.map(({ key, label }) => (
            <Section key={key} title={label} data={result[key]} />
          ))}

          {result.multi_llm_evaluation && (
            <div style={{ marginBottom: 12 }}>
              <div style={{
                fontSize: 12.5, color: 'var(--text3)', padding: '8px 14px',
                background: 'var(--bg3)', borderRadius: 'var(--radius-sm) var(--radius-sm) 0 0',
                borderLeft: '3px solid var(--text3)',
              }}>
                💡 <strong>Supplementary signal, not final</strong> — reflects overall resume
                strength across 3 LLMs. The Hiring Committee below makes the actual call
                and directly weighs the required-skill gap.
              </div>
              <Section title="Multi-LLM Evaluation (supplementary)" data={result.multi_llm_evaluation} />
            </div>
          )}

          {result.committee_result && (
            <div style={{ marginBottom: 12 }}>
              <div style={{
                fontSize: 12.5, color: 'var(--accent2)', padding: '8px 14px',
                background: 'rgba(0,212,170,0.08)', borderRadius: 'var(--radius-sm) var(--radius-sm) 0 0',
                borderLeft: '3px solid var(--accent2)', fontWeight: 600,
              }}>
                ✓ Authoritative — this decision (factoring in the required-skill gap directly)
                is what drives the Final Decision above.
              </div>
              <Section title="Hiring Committee Decision" data={result.committee_result} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}
