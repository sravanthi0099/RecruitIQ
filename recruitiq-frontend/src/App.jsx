import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import { ThemeProvider } from './ThemeContext';
import ProtectedLayout from './ProtectedLayout';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import CandidatesPage from './pages/CandidatesPage';
import JobsPage from './pages/JobsPage';
import MatchingPage from './pages/MatchingPage';
import AnalysisPage from './pages/AnalysisPage';
import InterviewPage from './pages/InterviewPage';
import CopilotPage from './pages/CopilotPage';
import AnalyticsPage from './pages/AnalyticsPage';
import InsightsPage from './pages/InsightsPage';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<ProtectedLayout><Dashboard /></ProtectedLayout>} />
            <Route path="/candidates" element={<ProtectedLayout><CandidatesPage /></ProtectedLayout>} />
            <Route path="/jobs" element={<ProtectedLayout><JobsPage /></ProtectedLayout>} />
            <Route path="/matching" element={<ProtectedLayout><MatchingPage /></ProtectedLayout>} />
            <Route path="/analysis" element={<ProtectedLayout><AnalysisPage /></ProtectedLayout>} />
            <Route path="/interview" element={<ProtectedLayout><InterviewPage /></ProtectedLayout>} />
            <Route path="/copilot" element={<ProtectedLayout><CopilotPage /></ProtectedLayout>} />
            <Route path="/analytics" element={<ProtectedLayout><AnalyticsPage /></ProtectedLayout>} />
            <Route path="/insights" element={<ProtectedLayout><InsightsPage /></ProtectedLayout>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
