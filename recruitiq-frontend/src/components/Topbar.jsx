import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Bell, Plus, User, Briefcase } from 'lucide-react';
import { getCandidates, getJobs } from '../api/endpoints';
import ThemeToggle from './ThemeToggle';

export default function Topbar() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [results, setResults] = useState({ candidates: [], jobs: [] });
  const [open, setOpen] = useState(false);
  const [showAddMenu, setShowAddMenu] = useState(false);
  const boxRef = useRef(null);
  const debounceRef = useRef(null);

  useEffect(() => {
    const onClickOutside = (e) => {
      if (boxRef.current && !boxRef.current.contains(e.target)) {
        setOpen(false);
        setShowAddMenu(false);
      }
    };
    document.addEventListener('mousedown', onClickOutside);
    return () => document.removeEventListener('mousedown', onClickOutside);
  }, []);

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (query.trim().length < 2) {
      setResults({ candidates: [], jobs: [] });
      return;
    }

    debounceRef.current = setTimeout(async () => {
      try {
        const [cRes, jRes] = await Promise.all([getCandidates(1, 50), getJobs()]);
        const q = query.trim().toLowerCase();

        const candidates = (cRes.data.candidates || [])
          .filter((c) => `${c.first_name} ${c.last_name}`.toLowerCase().includes(q))
          .slice(0, 5);

        const jobs = (jRes.data.jobs || [])
          .filter((j) => j.title?.toLowerCase().includes(q))
          .slice(0, 5);

        setResults({ candidates, jobs });
        setOpen(true);
      } catch {
        /* silent — quick search is a convenience, not critical path */
      }
    }, 300);

    return () => clearTimeout(debounceRef.current);
  }, [query]);

  const hasResults = results.candidates.length > 0 || results.jobs.length > 0;

  return (
    <div className="topbar">
      <div className="topbar-search" ref={boxRef}>
        <Search size={16} className="topbar-search-icon" />
        <input
          className="topbar-search-input"
          placeholder="Search candidates, jobs…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query.trim().length >= 2 && setOpen(true)}
        />

        {open && (
          <div className="topbar-search-dropdown">
            {!hasResults ? (
              <div className="topbar-search-empty">No matches yet — keep typing.</div>
            ) : (
              <>
                {results.candidates.length > 0 && (
                  <div className="topbar-search-group">
                    <div className="topbar-search-label">Candidates</div>
                    {results.candidates.map((c) => (
                      <button
                        key={c.id}
                        className="topbar-search-item"
                        onClick={() => { navigate('/candidates'); setOpen(false); setQuery(''); }}
                      >
                        <User size={14} /> {c.first_name} {c.last_name}
                      </button>
                    ))}
                  </div>
                )}
                {results.jobs.length > 0 && (
                  <div className="topbar-search-group">
                    <div className="topbar-search-label">Jobs</div>
                    {results.jobs.map((j) => (
                      <button
                        key={j.id}
                        className="topbar-search-item"
                        onClick={() => { navigate('/jobs'); setOpen(false); setQuery(''); }}
                      >
                        <Briefcase size={14} /> {j.title}
                      </button>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        )}
      </div>

      <div className="topbar-actions">
        <div style={{ position: 'relative' }}>
          <button
            className="btn btn-primary btn-sm animated-btn"
            onClick={() => setShowAddMenu((s) => !s)}
          >
            <Plus size={14} /> Quick Add
          </button>
          {showAddMenu && (
            <div className="topbar-add-menu">
              <button onClick={() => { navigate('/candidates'); setShowAddMenu(false); }}>
                <User size={14} /> New Candidate
              </button>
              <button onClick={() => { navigate('/jobs'); setShowAddMenu(false); }}>
                <Briefcase size={14} /> New Job
              </button>
            </div>
          )}
        </div>

        <button className="btn-icon-ghost" title="Notifications">
          <Bell size={17} />
          <span className="notif-dot" />
        </button>

        <ThemeToggle />
      </div>
    </div>
  );
}
