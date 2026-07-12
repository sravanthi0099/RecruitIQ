import { useEffect, useState } from 'react';
import { Plus, X, Briefcase, MapPin, DollarSign, Tag } from 'lucide-react';
import { getJobs, createJob } from '../api/endpoints';

function CreateJobModal({ onClose, onSuccess }) {
  const [form, setForm] = useState({
    title: '', description: '', requirements: '', nice_to_have: '',
    seniority_level: 'Junior', department: 'Engineering', location: 'Hyderabad',
    job_type: 'Full Time', salary_min: '', salary_max: '', currency: 'INR',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async () => {
    if (!form.title || !form.description) { setError('Title and description are required.'); return; }
    setLoading(true); setError('');
    try {
      const payload = {
        ...form,
        requirements: form.requirements.split(',').map(s => s.trim()).filter(Boolean),
        nice_to_have: form.nice_to_have.split(',').map(s => s.trim()).filter(Boolean),
        salary_min: form.salary_min ? Number(form.salary_min) : undefined,
        salary_max: form.salary_max ? Number(form.salary_max) : undefined,
      };
      await createJob(payload);
      onSuccess(); onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create job.');
    } finally { setLoading(false); }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" style={{ maxWidth: 640 }} onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Create New Job</h2>
          <button className="btn btn-icon btn-secondary" onClick={onClose}><X size={16} /></button>
        </div>
        {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          <div className="form-grid">
            <div className="input-group form-full">
              <label>Job Title *</label>
              <input className="input" placeholder="AI/ML Engineer" value={form.title} onChange={set('title')} />
            </div>
            <div className="input-group form-full">
              <label>Description *</label>
              <textarea className="textarea" placeholder="Describe the role and responsibilities…" value={form.description} onChange={set('description')} />
            </div>
            <div className="input-group form-full">
              <label>Requirements (comma-separated)</label>
              <input className="input" placeholder="Python, FastAPI, ML, Docker" value={form.requirements} onChange={set('requirements')} />
            </div>
            <div className="input-group form-full">
              <label>Nice to Have (comma-separated)</label>
              <input className="input" placeholder="Kubernetes, AWS" value={form.nice_to_have} onChange={set('nice_to_have')} />
            </div>
            <div className="input-group">
              <label>Seniority Level</label>
              <select className="select" value={form.seniority_level} onChange={set('seniority_level')}>
                <option>Junior</option><option>Mid</option><option>Senior</option><option>Lead</option>
              </select>
            </div>
            <div className="input-group">
              <label>Job Type</label>
              <select className="select" value={form.job_type} onChange={set('job_type')}>
                <option>Full Time</option><option>Part Time</option><option>Contract</option><option>Internship</option>
              </select>
            </div>
            <div className="input-group">
              <label>Department</label>
              <input className="input" placeholder="Engineering" value={form.department} onChange={set('department')} />
            </div>
            <div className="input-group">
              <label>Location</label>
              <input className="input" placeholder="Hyderabad" value={form.location} onChange={set('location')} />
            </div>
            <div className="input-group">
              <label>Min Salary (INR)</label>
              <input className="input" type="number" placeholder="600000" value={form.salary_min} onChange={set('salary_min')} />
            </div>
            <div className="input-group">
              <label>Max Salary (INR)</label>
              <input className="input" type="number" placeholder="1200000" value={form.salary_max} onChange={set('salary_max')} />
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Creating…' : 'Create Job'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function JobsPage() {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreate, setShowCreate] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await getJobs();
      setJobs(res.data.jobs || []);
    } catch (err) {
      setJobs([]);
      setError(
        err.response?.status === 401
          ? 'Your session has expired — please log in again.'
          : err.response?.data?.detail || 'Failed to load jobs. Is the backend running?'
      );
    }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const fmt = (n) => n != null ? `₹${(n / 100000).toFixed(1)}L` : null;

  return (
    <div>
      <div className="page-header-row page-header">
        <div>
          <h1>Jobs</h1>
          <p>{jobs.length} open positions</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowCreate(true)}>
          <Plus size={16} /> Post Job
        </button>
      </div>

      {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}

      {loading ? (
        <div className="loading-center"><div className="spinner" /><span>Loading jobs…</span></div>
      ) : jobs.length === 0 ? (
        <div className="empty-state">
          <Briefcase size={40} />
          <h3>No jobs posted yet</h3>
          <p>Create your first job posting to start receiving candidates.</p>
          <button className="btn btn-primary" onClick={() => setShowCreate(true)}><Plus size={14} /> Post Job</button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {jobs.map(job => (
            <div key={job.id} className="card" style={{ padding: '20px 24px' }}>
              <div className="flex justify-between items-center" style={{ marginBottom: 10 }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: 16 }}>{job.title}</div>
                  <div className="flex items-center gap-3 mt-1">
                    {job.department && (
                      <span className="text-sm text-muted flex items-center gap-2">
                        <Tag size={12} /> {job.department}
                      </span>
                    )}
                    {job.location && (
                      <span className="text-sm text-muted flex items-center gap-2">
                        <MapPin size={12} /> {job.location}
                      </span>
                    )}
                    {(job.salary_min || job.salary_max) && (
                      <span className="text-sm text-muted flex items-center gap-2">
                        <DollarSign size={12} />
                        {[fmt(job.salary_min), fmt(job.salary_max)].filter(Boolean).join(' – ')} {job.currency || 'INR'}
                      </span>
                    )}
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  {job.seniority_level && <span className="badge badge-purple">{job.seniority_level}</span>}
                  {job.job_type && <span className="badge badge-gray">{job.job_type}</span>}
                </div>
              </div>

              {job.description && (
                <p style={{ fontSize: 14, color: 'var(--text2)', marginBottom: 12, lineHeight: 1.6 }}>
                  {job.description.length > 200 ? job.description.slice(0, 200) + '…' : job.description}
                </p>
              )}

              {(job.requirements || []).length > 0 && (
                <div>
                  <div style={{ fontSize: 11, fontWeight: 600, letterSpacing: '0.8px', textTransform: 'uppercase', color: 'var(--text3)', marginBottom: 6 }}>
                    Requirements
                  </div>
                  <div className="tag-list">
                    {job.requirements.map(r => <span key={r} className="tag tag-accent">{r}</span>)}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {showCreate && <CreateJobModal onClose={() => setShowCreate(false)} onSuccess={load} />}
    </div>
  );
}
