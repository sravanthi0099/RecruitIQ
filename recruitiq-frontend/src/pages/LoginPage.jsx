import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/endpoints';
import { useAuth } from '../AuthContext';
import { Bot, Eye, EyeOff } from 'lucide-react';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(email, password);
      loginUser(res.data.access_token, res.data.user);
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid credentials. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center',
      background: 'var(--bg)', padding: 16,
    }}>
      {/* Background grid effect */}
      <div style={{
        position: 'fixed', inset: 0, pointerEvents: 'none',
        backgroundImage: 'linear-gradient(rgba(108,99,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(108,99,255,0.04) 1px, transparent 1px)',
        backgroundSize: '40px 40px',
      }} />

      <div style={{ width: '100%', maxWidth: 400, position: 'relative' }}>
        {/* Logo */}
        <div style={{ textAlign: 'center', marginBottom: 32 }}>
          <div style={{
            width: 56, height: 56, borderRadius: 14,
            background: 'linear-gradient(135deg, var(--accent), var(--accent2))',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            margin: '0 auto 14px', boxShadow: '0 8px 32px rgba(108,99,255,0.3)',
          }}>
            <Bot size={26} color="white" />
          </div>
          <h1 style={{ fontSize: 26, fontWeight: 700, fontFamily: "'Space Mono', monospace" }}>
            Recruit<span style={{ color: 'var(--accent)' }}>IQ</span>
          </h1>
          <p style={{ color: 'var(--text2)', fontSize: 14, marginTop: 4 }}>
            AI-Powered Recruitment Platform
          </p>
        </div>

        <div className="card" style={{ padding: '32px' }}>
          <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 6 }}>Welcome back</h2>
          <p style={{ color: 'var(--text2)', fontSize: 13, marginBottom: 24 }}>Sign in to your recruiter account</p>

          {error && (
            <div className="alert alert-danger" style={{ marginBottom: 16 }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <div className="input-group">
              <label>Email address</label>
              <input
                className="input"
                type="email"
                placeholder="you@company.com"
                value={email}
                onChange={e => setEmail(e.target.value)}
                required
                autoFocus
              />
            </div>
            <div className="input-group">
              <label>Password</label>
              <div style={{ position: 'relative' }}>
                <input
                  className="input"
                  type={showPw ? 'text' : 'password'}
                  placeholder="••••••••"
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  required
                  style={{ paddingRight: 42 }}
                />
                <button
                  type="button"
                  onClick={() => setShowPw(!showPw)}
                  style={{
                    position: 'absolute', right: 12, top: '50%', transform: 'translateY(-50%)',
                    background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text3)',
                    display: 'flex', alignItems: 'center',
                  }}
                >
                  {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <button className="btn btn-primary w-full" type="submit" disabled={loading} style={{ marginTop: 4, justifyContent: 'center', padding: '11px 18px' }}>
              {loading ? 'Signing in…' : 'Sign In'}
            </button>
          </form>
        </div>

        <p style={{ textAlign: 'center', color: 'var(--text3)', fontSize: 12, marginTop: 20 }}>
          RecruitIQ Multi-Agent System · Powered by Groq LLaMA
        </p>
      </div>
    </div>
  );
}
