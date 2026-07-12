import { useEffect, useState, useRef } from 'react';
import { Plus, Upload, Search, X, User } from 'lucide-react';
import { getCandidates, createCandidate, uploadResume } from '../api/endpoints';

const STATUS_BADGE = {
  new: 'badge-purple',
  screening: 'badge-teal',
  interview: 'badge-orange',
  offer: 'badge-teal',
  accepted: 'badge-teal',
  rejected: 'badge-red',
};

function AddCandidateModal({ onClose, onSuccess }) {
  const [form, setForm] = useState({ first_name: '', last_name: '', email: '', phone: '', location: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }));

  const handleSubmit = async () => {
    if (!form.first_name || !form.last_name || !form.email) {
      setError('First name, last name, and email are required.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await createCandidate(form);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create candidate.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Add New Candidate</h2>
          <button className="btn btn-icon btn-secondary" onClick={onClose}><X size={16} /></button>
        </div>
        {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}
        <div className="form-grid">
          <div className="input-group">
            <label>First Name *</label>
            <input className="input" placeholder="Sravanthi" value={form.first_name} onChange={set('first_name')} />
          </div>
          <div className="input-group">
            <label>Last Name *</label>
            <input className="input" placeholder="Danampalli" value={form.last_name} onChange={set('last_name')} />
          </div>
          <div className="input-group">
            <label>Email *</label>
            <input className="input" type="email" placeholder="candidate@email.com" value={form.email} onChange={set('email')} />
          </div>
          <div className="input-group">
            <label>Phone</label>
            <input className="input" placeholder="9398XXXXXX" value={form.phone} onChange={set('phone')} />
          </div>
          <div className="input-group form-full">
            <label>Location</label>
            <input className="input" placeholder="Hyderabad" value={form.location} onChange={set('location')} />
          </div>
        </div>
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={handleSubmit} disabled={loading}>
            {loading ? 'Creating…' : 'Create Candidate'}
          </button>
        </div>
      </div>
    </div>
  );
}

function UploadModal({ candidate, onClose, onSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fileRef = useRef();

  const handleUpload = async () => {
    if (!file) { setError('Please select a file first.'); return; }
    setLoading(true); setError('');
    try {
      await uploadResume(candidate.id, file);
      onSuccess();
      onClose();
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Upload Resume</h2>
          <button className="btn btn-icon btn-secondary" onClick={onClose}><X size={16} /></button>
        </div>
        <p style={{ color: 'var(--text2)', marginBottom: 20, fontSize: 14 }}>
          For <strong>{candidate.first_name} {candidate.last_name}</strong>
        </p>
        {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}
        <div
          onClick={() => fileRef.current.click()}
          style={{
            border: '2px dashed var(--border)', borderRadius: 'var(--radius)',
            padding: '40px 20px', textAlign: 'center', cursor: 'pointer',
            transition: 'border-color 0.15s',
            borderColor: file ? 'var(--accent)' : undefined,
          }}
        >
          <Upload size={28} style={{ color: 'var(--text3)', marginBottom: 10 }} />
          {file
            ? <p style={{ color: 'var(--accent)', fontWeight: 600 }}>{file.name}</p>
            : <><p style={{ fontWeight: 600 }}>Click to select resume</p><p style={{ color: 'var(--text3)', fontSize: 13 }}>PDF, DOCX supported</p></>
          }
          <input ref={fileRef} type="file" accept=".pdf,.docx,.doc" style={{ display: 'none' }} onChange={e => setFile(e.target.files[0])} />
        </div>
        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
          <button className="btn btn-primary" onClick={handleUpload} disabled={loading || !file}>
            {loading ? 'Uploading…' : 'Upload Resume'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function CandidatesPage() {
  const [candidates, setCandidates] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [showAdd, setShowAdd] = useState(false);
  const [uploadTarget, setUploadTarget] = useState(null);

  const load = async () => {
    setLoading(true);
    try {
      const res = await getCandidates(1, 50);
      setCandidates(res.data.candidates || []);
      setTotal(res.data.total || 0);
    } catch { setCandidates([]); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const filtered = candidates.filter(c =>
    `${c.first_name} ${c.last_name} ${c.email} ${c.location}`.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div>
      <div className="page-header-row page-header">
        <div>
          <h1>Candidates</h1>
          <p>{total} total candidates in your database</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowAdd(true)}>
          <Plus size={16} /> Add Candidate
        </button>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <div style={{ position: 'relative' }}>
          <Search size={15} style={{ position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)', color: 'var(--text3)' }} />
          <input
            className="input"
            style={{ paddingLeft: 36 }}
            placeholder="Search by name, email, location…"
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
        </div>
      </div>

      <div className="card">
        {loading ? (
          <div className="loading-center"><div className="spinner" /><span>Loading candidates…</span></div>
        ) : filtered.length === 0 ? (
          <div className="empty-state">
            <User size={40} />
            <h3>No candidates found</h3>
            <p>{search ? 'Try a different search term.' : 'Add your first candidate to get started.'}</p>
            {!search && <button className="btn btn-primary" onClick={() => setShowAdd(true)}><Plus size={14} /> Add Candidate</button>}
          </div>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Location</th>
                  <th>Experience</th>
                  <th>Skills</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map(c => (
                  <tr key={c.id}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <div style={{
                          width: 32, height: 32, borderRadius: '50%',
                          background: 'linear-gradient(135deg, var(--accent), var(--accent2))',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                          fontSize: 12, fontWeight: 700, color: 'white', flexShrink: 0,
                        }}>
                          {c.first_name?.[0]}{c.last_name?.[0]}
                        </div>
                        <div>
                          <div style={{ fontWeight: 600 }}>{c.first_name} {c.last_name}</div>
                        </div>
                      </div>
                    </td>
                    <td style={{ color: 'var(--text2)', fontSize: 13 }}>{c.email}</td>
                    <td style={{ color: 'var(--text2)', fontSize: 13 }}>{c.location || '—'}</td>
                    <td style={{ fontFamily: "'Space Mono', monospace", fontSize: 13 }}>
                      {c.years_of_experience != null ? `${c.years_of_experience} yrs` : '—'}
                    </td>
                    <td>
                      <div className="tag-list">
                        {(() => {
                          let skills = c.extracted_skills || [];
                          if (typeof skills === 'string') skills = skills.split(',').map(s => s.trim()).filter(Boolean);
                          if (!Array.isArray(skills)) skills = [];
                          return <>
                            {skills.slice(0, 3).map(s => <span key={s} className="tag">{s}</span>)}
                            {skills.length > 3 && <span className="tag">+{skills.length - 3}</span>}
                          </>;
                        })()}
                      </div>
                    </td>
                    <td>
                      <span className={`badge ${STATUS_BADGE[c.status] || 'badge-gray'}`}>
                        {c.status || 'new'}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary btn-sm"
                        onClick={() => setUploadTarget(c)}
                      >
                        <Upload size={13} /> Resume
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showAdd && <AddCandidateModal onClose={() => setShowAdd(false)} onSuccess={load} />}
      {uploadTarget && <UploadModal candidate={uploadTarget} onClose={() => setUploadTarget(null)} onSuccess={load} />}
    </div>
  );
}
