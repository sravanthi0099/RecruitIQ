import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import Sidebar from './components/Sidebar';
import Topbar from './components/Topbar';

export default function ProtectedLayout({ children }) {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return (
    <div className="app-layout">
      <Sidebar />
      <div className="main-col">
        <Topbar />
        <div className="main-content">{children}</div>
      </div>
    </div>
  );
}
