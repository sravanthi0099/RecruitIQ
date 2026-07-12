import { useEffect, useState } from 'react';
import { MessageSquare, Sparkles, Send, CheckCircle, Video } from 'lucide-react';
import { getJobs, getCandidates, generateQuestions, evaluateAnswer } from '../api/endpoints';
import LiveAnswerRecorder from '../components/LiveAnswerRecorder';

export default function InterviewPage() {
  const [jobs, setJobs] = useState([]);
  const [candidates, setCandidates] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [selectedCandidate, setSelectedCandidate] = useState('');
  const [difficulty, setDifficulty] = useState('medium');
  const [numQuestions, setNumQuestions] = useState(5);
  const [questions, setQuestions] = useState([]);
  const [genLoading, setGenLoading] = useState(false);
  const [dataLoading, setDataLoading] = useState(true);
  const [error, setError] = useState('');

  // Evaluation state
  const [activeQ, setActiveQ] = useState(null);
  const [answerMode, setAnswerMode] = useState('text'); // 'text' | 'voice'
  const [answer, setAnswer] = useState('');
  const [evalResults, setEvalResults] = useState({});
  const [evalLoading, setEvalLoading] = useState(false);

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

  const handleGenerate = async () => {
    if (!selectedCandidate || !selectedJob) { setError('Select both a candidate and a job.'); return; }
    setError(''); setGenLoading(true); setQuestions([]); setEvalResults({});
    try {
      const res = await generateQuestions(selectedCandidate, selectedJob, difficulty, numQuestions);
      setQuestions(res.data.questions || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate questions.');
    } finally { setGenLoading(false); }
  };

  const handleEvaluate = async (q) => {
    if (!answer.trim()) return;
    setEvalLoading(true);
    try {
      const res = await evaluateAnswer(selectedCandidate, selectedJob, q.question, answer);
      setEvalResults(prev => ({ ...prev, [q.question]: { ...res.data, answer } }));
      setActiveQ(null);
      setAnswer('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Evaluation failed.');
    } finally { setEvalLoading(false); }
  };

  const handleVoiceEvaluated = (q, result) => {
    setEvalResults(prev => ({ ...prev, [q.question]: { ...result, answer: result.transcript, mode: 'voice' } }));
    setActiveQ(null);
  };

  const recColor = (rec) => {
    if (!rec) return 'badge-gray';
    const r = rec.toLowerCase();
    if (r.includes('strong hire') || r.includes('hire')) return 'badge-teal';
    if (r.includes('no hire') || r.includes('reject')) return 'badge-red';
    return 'badge-orange';
  };

  if (dataLoading) return <div className="loading-center"><div className="spinner" /></div>;

  return (
    <div>
      <div className="page-header">
        <h1>Interview</h1>
        <p>Generate AI interview questions and evaluate candidate answers in real time</p>
      </div>

      {/* Config */}
      <div className="card" style={{ marginBottom: 20 }}>
        <div className="section-title">Configuration</div>
        <div className="form-grid">
          <div className="input-group">
            <label>Candidate</label>
            <select className="select" value={selectedCandidate} onChange={e => setSelectedCandidate(e.target.value)}>
              <option value="">— Select candidate —</option>
              {candidates.map(c => <option key={c.id} value={c.id}>{c.first_name} {c.last_name}</option>)}
            </select>
          </div>
          <div className="input-group">
            <label>Job</label>
            <select className="select" value={selectedJob} onChange={e => setSelectedJob(e.target.value)}>
              <option value="">— Select job —</option>
              {jobs.map(j => <option key={j.id} value={j.id}>{j.title}</option>)}
            </select>
          </div>
          <div className="input-group">
            <label>Difficulty</label>
            <select className="select" value={difficulty} onChange={e => setDifficulty(e.target.value)}>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
          <div className="input-group">
            <label>Number of Questions</label>
            <input className="input" type="number" min="1" max="20" value={numQuestions}
              onChange={e => setNumQuestions(Number(e.target.value))} />
          </div>
        </div>
        <div style={{ marginTop: 16 }}>
          <button className="btn btn-primary" onClick={handleGenerate} disabled={genLoading}>
            {genLoading ? 'Generating…' : <><Sparkles size={15} /> Generate Questions</>}
          </button>
        </div>
        {error && <div className="alert alert-danger" style={{ marginTop: 14 }}>{error}</div>}
      </div>

      {/* Questions */}
      {questions.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {questions.map((q, i) => {
            const evaluated = evalResults[q.question];
            return (
              <div key={i} className="card">
                <div className="flex justify-between items-center" style={{ marginBottom: 12 }}>
                  <div className="flex items-center gap-3">
                    <div style={{
                      width: 28, height: 28, borderRadius: '50%',
                      background: evaluated ? 'rgba(0,212,170,0.15)' : 'rgba(108,99,255,0.15)',
                      color: evaluated ? 'var(--accent2)' : 'var(--accent)',
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      fontSize: 12, fontWeight: 700, flexShrink: 0,
                    }}>
                      {evaluated ? <CheckCircle size={14} /> : i + 1}
                    </div>
                    <div>
                      {q.topic && <span className="badge badge-purple" style={{ fontSize: 11 }}>{q.topic}</span>}
                      {' '}
                      {q.difficulty && <span className="badge badge-gray" style={{ fontSize: 11 }}>{q.difficulty}</span>}
                    </div>
                  </div>
                  {evaluated && (
                    <div className="flex items-center gap-2">
                      <span className="font-mono" style={{ fontSize: 14, fontWeight: 700, color: 'var(--accent2)' }}>
                        {evaluated.overall_score}/100
                      </span>
                      <span className={`badge ${recColor(evaluated.recommendation)}`} style={{ fontSize: 11 }}>
                        {evaluated.recommendation}
                      </span>
                    </div>
                  )}
                </div>

                <p style={{ fontSize: 15, fontWeight: 500, marginBottom: 14, lineHeight: 1.6 }}>
                  {q.question}
                </p>

                {evaluated ? (
                  <div>
                    <div style={{ fontSize: 13, color: 'var(--text2)', background: 'var(--bg3)', padding: '10px 14px', borderRadius: 'var(--radius-sm)', marginBottom: 10 }}>
                      <strong style={{ color: 'var(--text3)' }}>
                        {evaluated.mode === 'voice' ? <><Video size={12} style={{ verticalAlign: -2 }} /> Live voice answer (transcribed):</> : 'Answer given:'}
                      </strong> {evaluated.answer}
                    </div>
                    {evaluated.mode === 'voice' && (
                      <div className="flex gap-2" style={{ marginBottom: 10, flexWrap: 'wrap' }}>
                        <span className="badge badge-gray" style={{ fontSize: 11 }}>{evaluated.speaking_pace_wpm} wpm</span>
                        <span className="badge badge-gray" style={{ fontSize: 11 }}>{evaluated.filler_word_count} filler words</span>
                        <span className="badge badge-gray" style={{ fontSize: 11 }}>{evaluated.long_pause_count} long pauses</span>
                        {evaluated.eye_contact_score != null && (
                          <span className="badge badge-gray" style={{ fontSize: 11 }}>{evaluated.eye_contact_score}% eye contact</span>
                        )}
                      </div>
                    )}
                    <div
  style={{
    display: 'grid',
    gridTemplateColumns: 'repeat(4,1fr)',
    gap: '10px',
    marginBottom: '12px'
  }}
>
  <div className="card">
    <strong>Technical</strong>
    <br />
    {evaluated.technical_score}
  </div>

  <div className="card">
    <strong>Communication</strong>
    <br />
    {evaluated.communication_score}
  </div>

  <div className="card">
    <strong>Problem Solving</strong>
    <br />
    {evaluated.problem_solving_score}
  </div>

  <div className="card">
    <strong>Confidence</strong>
    <br />
    {evaluated.confidence_score}
  </div>
</div>

{evaluated.feedback && (
  <div className="alert alert-success">
    <MessageSquare size={15} style={{ flexShrink: 0, marginTop: 2 }} />
    <div>
      <strong>AI Feedback:</strong> {evaluated.feedback}
    </div>
  </div>
)}
                  </div>
                ) : activeQ === i ? (
                  <div>
                    <div className="flex gap-2" style={{ marginBottom: 12 }}>
                      <button
                        className={`btn btn-sm ${answerMode === 'text' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setAnswerMode('text')}
                      >
                        <MessageSquare size={13} /> Type Answer
                      </button>
                      <button
                        className={`btn btn-sm ${answerMode === 'voice' ? 'btn-primary' : 'btn-secondary'}`}
                        onClick={() => setAnswerMode('voice')}
                      >
                        <Video size={13} /> Live Voice + Camera
                      </button>
                    </div>

                    {answerMode === 'text' ? (
                      <>
                        <textarea
                          className="textarea"
                          placeholder="Type the candidate's answer here…"
                          value={answer}
                          onChange={e => setAnswer(e.target.value)}
                          style={{ marginBottom: 10 }}
                        />
                        <div className="flex gap-2">
                          <button className="btn btn-primary btn-sm" onClick={() => handleEvaluate(q)} disabled={evalLoading || !answer.trim()}>
                            {evalLoading ? 'Evaluating…' : <><Send size={13} /> Evaluate</>}
                          </button>
                          <button className="btn btn-secondary btn-sm" onClick={() => { setActiveQ(null); setAnswer(''); }}>
                            Cancel
                          </button>
                        </div>
                      </>
                    ) : (
                      <>
                        <LiveAnswerRecorder
                          candidateId={selectedCandidate}
                          jobId={selectedJob}
                          question={q.question}
                          onEvaluated={(result) => handleVoiceEvaluated(q, result)}
                        />
                        <button className="btn btn-secondary btn-sm" style={{ marginTop: 10 }} onClick={() => setActiveQ(null)}>
                          Cancel
                        </button>
                      </>
                    )}
                  </div>
                ) : (
                  <button className="btn btn-secondary btn-sm" onClick={() => setActiveQ(i)}>
                    <MessageSquare size={13} /> Enter Answer & Evaluate
                  </button>
                )}
              </div>
            );
          })}
        </div>
      )}

      {questions.length === 0 && !genLoading && (
        <div className="empty-state">
          <MessageSquare size={40} />
          <h3>No questions yet</h3>
          <p>Configure the settings above and generate AI-powered interview questions.</p>
        </div>
      )}
    </div>
  );
}