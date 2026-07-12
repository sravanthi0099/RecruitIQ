import { useState, useRef, useEffect } from 'react';
import { Bot, Send, User, Lightbulb } from 'lucide-react';
import { askCopilot } from '../api/endpoints';

const SUGGESTIONS = [
  'Who is the strongest match for the AI Engineer role?',
  'Summarize the top 3 candidates by skill match',
  'Which candidates have Python and FastAPI experience?',
  'What are the skill gaps across all candidates?',
  'Who should I prioritize for the next interview round?',
];

export default function CopilotPage() {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      text: "Hi! I'm your AI Recruiter Copilot 🤖 Ask me anything about your candidates, jobs, or hiring pipeline — I'll give you intelligent insights instantly.",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const question = text || input.trim();
    if (!question || loading) return;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: question }]);
    setLoading(true);
    try {
      const res = await askCopilot(question);
      setMessages(prev => [
  ...prev,
  {
    role: 'bot',
    text:
  `🎯 Answer:\n${res.data.answer || 'N/A'}\n\n` +
  `🧠 Reasoning:\n${res.data.reasoning || 'N/A'}\n\n` +
  `✅ Recommendation:\n${res.data.recommendation || 'N/A'}`
  }
]);
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'bot',
        text: '⚠️ Sorry, I encountered an error. Please check your backend connection and try again.',
      }]);
    } finally { setLoading(false); }
  };

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Recruiter Copilot</h1>
        <p>Your AI assistant for intelligent hiring decisions</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 280px', gap: 20, height: 'calc(100vh - 180px)' }}>
        {/* Chat */}
        <div className="card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden' }}>
          <div style={{
            padding: '16px 20px', borderBottom: '1px solid var(--border)',
            display: 'flex', alignItems: 'center', gap: 10,
          }}>
            <div style={{
              width: 36, height: 36, borderRadius: '50%',
              background: 'linear-gradient(135deg, var(--accent), var(--accent2))',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <Bot size={18} color="white" />
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: 14 }}>Recruiter Copilot</div>
              <div style={{ fontSize: 12, color: 'var(--accent2)' }}>● Online</div>
            </div>
          </div>

          {/* Messages */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '20px', display: 'flex', flexDirection: 'column', gap: 14 }}>
            {messages.map((msg, i) => (
              <div key={i} className={`chat-msg ${msg.role}`}>
                <div className={`chat-avatar ${msg.role}`}>
                  {msg.role === 'bot' ? <Bot size={15} /> : <User size={15} />}
                </div>
                <div className="chat-bubble" style={{ whiteSpace: 'pre-wrap' }}>
                  {msg.text}
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-msg bot">
                <div className="chat-avatar bot"><Bot size={15} /></div>
                <div className="chat-bubble">
                  <span style={{ display: 'inline-flex', gap: 4, alignItems: 'center' }}>
                    <span style={{ animation: 'pulse 1s infinite', animationDelay: '0s' }}>●</span>
                    <span style={{ animation: 'pulse 1s infinite', animationDelay: '0.2s' }}>●</span>
                    <span style={{ animation: 'pulse 1s infinite', animationDelay: '0.4s' }}>●</span>
                  </span>
                </div>
              </div>
            )}
            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div style={{ padding: '14px 20px', borderTop: '1px solid var(--border)' }}>
            <div className="chat-input-row" style={{ margin: 0 }}>
              <textarea
                className="input"
                placeholder="Ask about candidates, skills, or hiring decisions…"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={handleKey}
                rows={2}
                style={{ resize: 'none' }}
              />
              <button
                className="btn btn-primary"
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
                style={{ alignSelf: 'flex-end', padding: '10px 16px' }}
              >
                <Send size={16} />
              </button>
            </div>
            <div style={{ fontSize: 11, color: 'var(--text3)', marginTop: 6 }}>Press Enter to send · Shift+Enter for new line</div>
          </div>
        </div>

        {/* Suggestions */}
        <div>
          <div className="card">
            <div className="flex items-center gap-2" style={{ marginBottom: 14 }}>
              <Lightbulb size={16} style={{ color: 'var(--warn)' }} />
              <div className="section-title" style={{ margin: 0 }}>Suggested Questions</div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {SUGGESTIONS.map((s, i) => (
                <button
                  key={i}
                  className="btn btn-secondary"
                  onClick={() => sendMessage(s)}
                  disabled={loading}
                  style={{ textAlign: 'left', justifyContent: 'flex-start', fontSize: 13, padding: '10px 12px', lineHeight: 1.4 }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="card" style={{ marginTop: 14 }}>
            <div className="section-title">Tips</div>
            <ul style={{ fontSize: 13, color: 'var(--text2)', lineHeight: 1.8, paddingLeft: 16, margin: 0 }}>
              <li>Ask about specific candidates by name</li>
              <li>Request skill comparisons</li>
              <li>Ask for interview recommendations</li>
              <li>Get salary benchmarks</li>
            </ul>
          </div>
        </div>
      </div>

      <style>{`@keyframes pulse { 0%,100% { opacity:0.3; } 50% { opacity:1; } }`}</style>
    </div>
  );
}
