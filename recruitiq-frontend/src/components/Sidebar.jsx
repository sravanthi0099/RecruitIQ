import { NavLink, useNavigate } from 'react-router-dom';
import {
  LayoutDashboard, Users, Briefcase, Target, FlaskConical,
  MessageSquare, BarChart2, LogOut, Bot, Gauge
} from 'lucide-react';
import { useAuth } from '../AuthContext';

const nav = [
  { label: 'Core', items: [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/candidates', icon: Users, label: 'Candidates' },
    { to: '/jobs', icon: Briefcase, label: 'Jobs' },
  ]},
  { label: 'AI Modules', items: [
    { to: '/matching', icon: Target, label: 'Matching Center' },
    { to: '/analysis', icon: FlaskConical, label: 'Full Analysis' },
    { to: '/interview', icon: MessageSquare, label: 'Interview' },
    { to: '/copilot', icon: Bot, label: 'Recruiter Copilot' },
  ]},
  { label: 'Insights', items: [
    { to: '/analytics', icon: BarChart2, label: 'Analytics' },
    { to: '/insights', icon: Gauge, label: 'Insights Hub' },
  ]},
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => { logout(); navigate('/login'); };

  const initials = user?.full_name
    ? user.full_name.split(' ').map(n => n[0]).join('').slice(0, 2).toUpperCase()
    : 'U';

  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div className="logo-icon">IQ</div>
        <div className="logo-text">Recruit<span>IQ</span></div>
      </div>

      {nav.map((section) => (
        <div key={section.label}>
          <div className="sidebar-section-label">{section.label}</div>
          {section.items.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
            >
              <Icon size={16} />
              {label}
            </NavLink>
          ))}
        </div>
      ))}

      <div className="sidebar-footer">
        <div className="sidebar-user">
          <div className="avatar">{initials}</div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
              {user?.full_name || 'Recruiter'}
            </div>
            <div style={{ fontSize: 11, color: 'var(--text3)', textTransform: 'capitalize' }}>{user?.role || 'recruiter'}</div>
          </div>
          <button className="btn btn-icon btn-secondary" onClick={handleLogout} title="Logout">
            <LogOut size={14} />
          </button>
        </div>
      </div>
    </div>
  );
}
